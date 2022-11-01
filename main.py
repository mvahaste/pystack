from venv import create
import pygame


def new_box(pos: list, size: list, speed: int):
    return Box([pos[0], SCREEN_Y - 50 - pos[1]], size, speed)


class Box:
    def __init__(self, pos, size, speed):
        self.pos = pos
        self.size = size
        self.speed = speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def move(self):
        left = self.pos[0]
        right = self.pos[0] + self.size[0]

        if left < 0 or right > SCREEN_X:
            self.speed *= -1

        self.pos[0] += self.speed


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
# TODO: win condition, resize box, lose condition, sfx, visuals

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Sound
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("pyStack")
clock = pygame.time.Clock()  # Sync FPS

current_box = new_box([0, 0], [150, 20], 1)

tower = []


while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                tower.append(current_box)

                if len(tower) > 1:
                    last_box = tower[-1]
                    last_last_box = tower[-2]

                    last_left = last_box.pos[0]
                    last_right = last_box.pos[0] + last_box.size[0]

                    last_last_left = last_last_box.pos[0]
                    last_last_right = last_last_box.pos[0] + last_last_box.size[0]

                    if last_left <= last_last_left:
                        last_left = last_last_left
                    elif last_left 

                    print(f"LAST BOX: X1 {last_left} X2 {last_right}\nLAST LAST BOX: X1 {last_last_left} X2 {last_last_right}")

                current_box = new_box([0, len(tower) * 20], [150, 20], 1)

        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BLACK)

    current_box.draw()
    current_box.move()

    for box in tower:
        box.draw()

    pygame.display.flip()