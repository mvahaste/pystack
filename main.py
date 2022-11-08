from venv import create
import pygame


def new_box(x: int, y: int, w: int, h: int, speed: int):
    return Box(x, SCREEN_Y - 50 - y, w, h, speed)


class Box:
    def __init__(self, x: int, y: int, w: int, h: int, speed: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x, self.y, self.w, self.h))

    def move(self):
        left = self.x
        right = self.x + self.w

        if left < 0 or right > SCREEN_X:
            self.speed *= -1

        self.x += self.speed


SCREEN_X = 480
SCREEN_Y = 640
RESOLUTION = (SCREEN_X, SCREEN_Y)
FPS = 60

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ! SELF MADE SFX
# TODO: resize box, win/lose condition, visuals, sfx

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Sound
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("pyStack")
clock = pygame.time.Clock()  # Sync FPS

player = new_box(0, 0, 180, 20, 3)

tower = []


tower.append(Box((SCREEN_X / 2) - 90, player.y + 20, 180, player.h, 1))

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                last_box = tower[-1]

                current_left = player.x
                current_right = player.x + player.w

                last_left = last_box.x
                last_right = last_box.x + last_box.w

                # * Overlap left
                if current_left < last_left:
                    player.x = last_box.x
                    player.w -= last_right - current_right

                # * Overlap right
                elif current_right > last_right:
                    player.w -= current_right - last_right

                tower.append(Box(player.x, player.y, player.w, player.h, 1))

                player.y -= 20
                player.x = 0

                print([box.w for box in tower])

        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BLACK)

    player.draw()
    player.move()

    for box in tower:
        box.draw()

    pygame.display.flip()
