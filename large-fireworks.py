# This is the same idea as the minimal script, taken into a window. I draw
# one burst per frame in pygame instead of printing rows, and I put the
# stick figure next to each burst so the scene has a witness.
import random
from pathlib import Path

import pygame

# I sized the window at 700 by 500 and then wrote the random ranges in
# main from these numbers. If I change SIZE, I have to change those ranges
# too, or bursts will cluster in one corner of a bigger window.
SIZE = (700, 500)
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0),
          (0, 0, 255), (75, 0, 130), (238, 130, 238)]


def draw_firework(screen, x, y, color, radius, trail_color, trail_length):
    # The "trail" is a ring, not a streak: draw.circle with a width draws
    # an outline that grows inward from the radius. I draw the filled
    # circle second, over the ring's inside, so what survives on screen is
    # the ring's outer band in the darker shade around the bright disc.
    # If I draw them in the other order, the trail disappears entirely.
    # One catch I live with: when trail_length is close to radius, the
    # ring is almost solid, so small bursts can look like two flat discs.
    pygame.draw.circle(screen, trail_color, (x, y), radius, trail_length)
    pygame.draw.circle(screen, color, (x, y), radius)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Fireworks")

    # I look the image up next to this script, not in the caller's working
    # directory. The first version used a bare relative path, so launching
    # the script from any other folder crashed before the window opened.
    # If stick_figure.png is missing, I still crash here at load time. I
    # accept that, because the program has nothing sensible to show
    # without the figure, and the error names the missing file.
    stick_figure = pygame.image.load(
        str(Path(__file__).parent / "stick_figure.png"))
    stick_figure_rect = stick_figure.get_rect()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))

        # Nothing persists between frames: I wipe the screen and draw
        # exactly one new firework, so the show is a strobe of single
        # bursts rather than a sky that fills up.
        # I keep the center at least 50 pixels from each edge. The largest
        # radius I allow below is also 50, so a big burst can touch the
        # edge but its center never starts outside the window.
        x = random.randint(50, 650)
        y = random.randint(50, 450)
        color = random.choice(COLORS)
        radius = random.randint(10, 50)
        # I halve each channel to keep the trail the same hue as its
        # burst. Integer division rounds down, so odd values lose a step.
        # I do not mind, because the trail only needs to read as darker.
        trail_color = (color[0] // 2, color[1] // 2, color[2] // 2)
        trail_length = random.randint(5, 15)
        draw_firework(screen, x, y, color, radius, trail_color, trail_length)

        # I place the figure up and to the left of the burst center by its
        # own size, plus 30 pixels, so it reads as standing beside the
        # burst rather than inside it. Near the top or left edge that
        # offset can push part of the figure off screen. I leave that as
        # is, because pygame clips the blit and the next frame moves on.
        screen.blit(stick_figure,
                    (x - stick_figure_rect.width,
                     y - stick_figure_rect.height - 30))

        pygame.display.flip()

        # I use no clock object, so this wait is the whole frame limiter.
        # It also caps how often I read the event queue, which is why the
        # window can take a beat to notice a close click.
        pygame.time.wait(100)

    pygame.quit()


if __name__ == "__main__":
    main()
