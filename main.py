import pygame
from random import choice


def create_box(x: int, y: int, w: int, h: int, speed: int, color: tuple):
    return Box(x, SCREEN_Y - 50 - y, w, h, speed, color)


class Box:
    def __init__(self, x: int, y: int, w: int, h: int, speed: int, color: tuple):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h))

    def move(self):
        left = self.x
        right = self.x + self.w

        if left < 0 or right > SCREEN_X:
            self.speed *= -1

            bounce_sound.play()

        self.x += self.speed


class Colors:
    def __init__(self) -> None:
        self.gradient = [
            (25, 118, 210),
            (28, 112, 205),
            (31, 106, 199),
            (34, 100, 194),
            (37, 94, 188),
            (39, 88, 183),
            (42, 81, 177),
            (44, 75, 171),
            (46, 69, 165),
            (48, 63, 159),
            (46, 69, 165),
            (44, 75, 171),
            (42, 81, 177),
            (39, 88, 183),
            (37, 94, 188),
            (34, 100, 194),
            (31, 106, 199),
            (28, 112, 205),
            (25, 118, 210),
        ]
        self.gradient_index = 0

    def gradient_color(self):
        self.gradient_index += 1

        if self.gradient_index >= len(self.gradient):
            self.gradient_index = 0

        return self.gradient[self.gradient_index]


SCREEN_X = 480
SCREEN_Y = 640
RESOLUTION = (SCREEN_X, SCREEN_Y)
FPS = 60

# Define Colors
BACKGROUND = (15, 15, 15)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# TODO: visuals, sfx

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Sound
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("pyStack")
clock = pygame.time.Clock()  # Sync FPS

place_sound = pygame.mixer.Sound("place.wav")
loss_sound = pygame.mixer.Sound("loss.wav")
bounce_sound = pygame.mixer.Sound("bounce.wav")

color_manager = Colors()

score = 0

status = "playing"

# Tower
tower = []

for i in range(1, 11):
    tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y - (30 * i), 240, 30, 1, color_manager.gradient_color()))

# Player
player = create_box(0, 0, 240, 30, 4, color_manager.gradient_color())
player.y = tower[-1].y - 30

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 32:
                if status == "playing":
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

                    if player.w <= 0:
                        print("You lose!")
                        status = "lost"
                        loss_sound.play()
                    else:
                        place_sound.play()

                    tower.append(Box(player.x, player.y, player.w, player.h, 0, player.color))

                    for box in tower:
                        box.y += 30

                    # Move the player to the left or right side of the screen
                    player.x = choice([0, SCREEN_X - player.w])

                    # Set the speed to the correct direction so the box doesn't bounce the instant it spawns
                    if player.x == 0:
                        player.speed = 4
                    elif player.x == SCREEN_X - player.w:
                        player.speed = -4

                    player.color = color_manager.gradient_color()

                    score += 1
                    print(f"Score: {score}; Speed: {player.speed}")
                elif status == "lost":
                    # Reset the game
                    status = "playing"
                    tower = []

                    for i in range(1, 11):
                        tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y - (30 * i), 240, 30, 1, color_manager.gradient_color()))

                    player = create_box(0, 0, 240, 30, 4, color_manager.gradient_color())
                    player.y = tower[-1].y - 30
                    score = 0

        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BACKGROUND)

    player.draw()
    player.move()

    for box in tower:
        box.draw()

    pygame.display.flip()
