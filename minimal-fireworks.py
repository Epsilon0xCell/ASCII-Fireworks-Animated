# I kept this version as small as I could. There is no grid, no position
# tracking, and no burst shape. I print one row at a time and I let the
# terminal scrolling do the rest of the work.
import random
import time

RESET = "\033[0m"
# I left blue and cyan out on purpose. On the dark terminal I ran this on,
# red, green, yellow, and magenta read clearly, and a short list keeps one
# color from repeating so often that the rows blur together.
COLORS = ["\033[31m", "\033[32m", "\033[33m", "\033[35m"]


def random_color():
    return random.choice(COLORS)


def firework():
    # I do not reset the color at the end of a row. The next row starts
    # with its own color code, so a reset in between would only add bytes.
    # That choice is why main has to print RESET once when the loop ends.
    # flush=True matters more than it looks: when stdout is a pipe instead
    # of a terminal, Python block-buffers it, and this loop would appear to
    # print nothing for minutes while the buffer fills. On a terminal the
    # flush is a no-op. I want the animation to behave the same in both.
    # I picked 5 to 15 stars because shorter rows vanished in the scroll
    # and longer rows just looked like a solid bar.
    print(random_color() + "*" * random.randint(5, 15), flush=True)


def main():
    try:
        while True:
            firework()
            # This sleep is the frame rate. Without it the loop prints as
            # fast as Python can, the terminal scrolls past too quickly to
            # read as fireworks, and one core stays pinned.
            time.sleep(0.1)
    except KeyboardInterrupt:
        # I catch Ctrl+C here instead of letting the traceback out. Leave
        # the terminal the way it was found: without the reset code the
        # last firework's color stays active in the user's prompt.
        print(RESET)
        return


if __name__ == "__main__":
    main()
