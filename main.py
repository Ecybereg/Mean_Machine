import os
import time
import subprocess

try:
    import pyfiglet
    from colorama import Fore, Style
except ImportError:
    print("Installing required libraries...")
    os.system('pip install pyfiglet colorama')
    print("Libraries installed. Please run the script again.")
    exit()

def print_banner():
    custom_fig = pyfiglet.Figlet(font='bubble')
    banner = custom_fig.renderText("Mean Machine")
    print(Fore.GREEN + banner)
    print(Fore.WHITE + f"All rights reserved to Erel Regev © {time.strftime('%Y')}")
    print("THIS DEVICE AND TOOLS WERE BUILT FOR EDUCATIONAL PURPOSES ONLY!!!")
    print("Version 1.1\n" + Style.RESET_ALL)

def menu():
    print("Choose an option:")
    print("1. Wi-Fi Cracker")
    print("2. Evil Portal")
    print("3. Option 3")
    print("4. Option 4")
    print("0. Exit")

def run_option(option):
    if option == '1':
        subprocess.run(['python', 'script1.py'])
    elif option == '2':
        subprocess.run(['python', 'script2.py'])
    elif option == '3':
        subprocess.run(['python', 'script3.py'])
    elif option == '4':
        subprocess.run(['python', 'script4.py'])
    elif option == '0':
        print("Exiting...")
        exit()
    else:
        print("Invalid option. Please try again.")

if __name__ == "__main__":
    print_banner()
    
    for _ in range(5, 0, -1):
        print(f"\rMenu will appear in {_} seconds...", end="")
        time.sleep(1)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        menu()
        user_option = input("Enter your choice: ")
        run_option(user_option)
