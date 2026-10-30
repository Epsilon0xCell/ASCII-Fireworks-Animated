import random
from pathlib import Path

import pygame

SIZE = (700, 500)
COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0),
          (0, 0, 255), (75, 0, 130), (238, 130, 238)]


def draw_firework(screen, x, y, color, radius, trail_color, trail_length):
    # The "trail" is a ring, not a streak: draw.circle with a width draws
    # an outline that grows inward from the radius. The filled circle is
    # drawn second, over the ring's inside, so what survives on screen is
    # the ring's outer band in the darker shade around the bright disc.
    # Draw them in the other order and the trail disappears entirely.
    pygame.draw.circle(screen, trail_color, (x, y), radius, trail_length)
    pygame.draw.circle(screen, color, (x, y), radius)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Fireworks")

    # The image is looked up next to this script, not in the caller's
    # working directory. The first version used a bare relative path, so
    # launching the script from any other folder crashed before the
    # window ever opened.
    stick_figure = pygame.image.load(
        str(Path(__file__).parent / "stick_figure.png"))
    stick_figure_rect = stick_figure.get_rect()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((0, 0, 0))

        # Nothing persists between frames: the screen is wiped and exactly
        # one new firework is drawn, so the show is a strobe of single
        # bursts rather than a sky that fills up.
        x = random.randint(50, 650)
        y = random.randint(50, 450)
        color = random.choice(COLORS)
        radius = random.randint(10, 50)
        # Halving each channel keeps the trail the same hue as its burst.
        trail_color = (color[0] // 2, color[1] // 2, color[2] // 2)
        trail_length = random.randint(5, 15)
        draw_firework(screen, x, y, color, radius, trail_color, trail_length)

        # The figure is placed up and to the left of the burst center by
        # its own size, plus 30 pixels, so it reads as standing beside the
        # burst rather than inside it.
        screen.blit(stick_figure,
                    (x - stick_figure_rect.width,
                     y - stick_figure_rect.height - 30))

        pygame.display.flip()

        # There is no clock object; this wait is the whole frame limiter.
        # It also caps how often the event queue is read, which is why the
        # window can take a beat to notice a close click.
        pygame.time.wait(100)

    pygame.quit()


if __name__ == "__main__":
    main()
