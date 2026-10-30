import random
import time

RESET = "\033[0m"
COLORS = ["\033[31m", "\033[32m", "\033[33m", "\033[35m"]


def random_color():
    return random.choice(COLORS)


def firework():
    # flush=True matters more than it looks: when stdout is a pipe instead
    # of a terminal, Python block-buffers it, and this loop would appear to
    # print nothing for minutes while the buffer fills. On a terminal the
    # flush is a no-op. The animation should behave the same in both.
    print(random_color() + "*" * random.randint(5, 15), flush=True)


def main():
    try:
        while True:
            firework()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Leave the terminal the way it was found: without the reset code
        # the last firework's color stays active in the user's prompt.
        print(RESET)
        return


if __name__ == "__main__":
    main()
