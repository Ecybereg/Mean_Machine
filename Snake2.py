import curses
import random

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)

    snake_speed = 10
    timeout = 150  # Set a fixed timeout value

    w.timeout(timeout)

    snake = [[sh//2, sw//2]]
    food = [random.randint(1, sh-1), random.randint(1, sw-1)]

    key = curses.KEY_RIGHT

    score = 0

    def display_score():
        w.addstr(0, 2, 'Score: {}'.format(score))

    def game_over():
        w.addstr(sh//2, sw//2 - 10, 'MEAN MACHINE WON. GO BACK TO HACKING.', curses.A_BOLD)
        w.addstr(sh//2 + 1, sw//2 - 20, 'Press Q to Quit or C to Play Again', curses.A_BOLD)
        w.refresh()

        while True:
            choice = w.getch()
            if choice == ord('q'):
                return False
            elif choice == ord('c'):
                return True

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
            if not game_over():
                break

            snake = [[sh//2, sw//2]]
            food = [random.randint(1, sh-1), random.randint(1, sw-1)]
            score = 0
            snake_speed = 10
            timeout = 700
            w.timeout(timeout)

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] == food:
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh-1),
                    random.randint(1, sw-1)
                ]
                food = nf if nf not in snake else None
            score += 1
            snake_speed += 1
            timeout = max(50, 150 - snake_speed * 5)  # Adjust timeout based on snake_speed
            w.timeout(timeout)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], '*', curses.color_pair(2))
        w.addch(food[0], food[1], '#')

        display_score()
        w.refresh()

    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
