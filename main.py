import pygame
from random import choice


def create_box(x: int, y: int, w: int, h: int, speed: int, color: tuple):
    return Box(x, SCREEN_Y - 50 - y, w, h, speed, color)


class Box:
    def __init__(self, x: int, y: int, w: int, h: int, speed: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.color = color

    def draw(self) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h), 1)

    def move(self) -> None:
        left = self.x
        right = self.x + self.w

        if left < 0 or right > SCREEN_X:
            self.speed *= -1

            bounce_sound.play()

        self.x += self.speed


class Colors:
    def __init__(self) -> None:
        self.gradient = [
            (156, 79, 150),
            (255, 99, 85),
            (251, 169, 73),
            (250, 228, 66),
            (139, 212, 72),
            (42, 168, 242),
            (139, 212, 72),
            (250, 228, 66),
            (251, 169, 73),
            (255, 99, 85),
        ]

        self.gradient_index = 0

    def gradient_color(self) -> tuple:
        self.gradient_index += 1

        if self.gradient_index >= len(self.gradient):
            self.gradient_index = 0

        return self.gradient[self.gradient_index]


class Button:
    def __init__(self, x, y, image, hover_image) -> None:
        self.image = pygame.transform.scale(
            image, (int(image.get_width()*0.6), int(image.get_height()*0.6)))
        self.hover = pygame.transform.scale(
            hover_image, (int(hover_image.get_width()*0.6), int(hover_image.get_height()*0.6)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pressed = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        image = self.image

        if self.rect.collidepoint(mouse_pos):
            image = self.hover
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.pressed = False

        screen.blit(image, (self.rect.x, self.rect.y))

        return self.pressed


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

# TODO: visuals, sfx

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Sound
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("pyStack")
clock = pygame.time.Clock()  # Sync FPS

place_sound = pygame.mixer.Sound("place.wav")
place_sound.set_volume(0.25)
loss_sound = pygame.mixer.Sound("loss.wav")
loss_sound.set_volume(0.25)
bounce_sound = pygame.mixer.Sound("bounce.wav")
bounce_sound.set_volume(0.25)

color_manager = Colors()

score = 0

status = "playing"

retry_img = pygame.image.load('retry.png').convert_alpha()
retry_hover = pygame.image.load('retry_hover.png').convert_alpha()
exit_img = pygame.image.load('quit.png').convert_alpha()
exit_hover = pygame.image.load('quit_hover.png').convert_alpha()

retry_button = Button(50, 550, retry_img, retry_hover)
exit_button = Button(250, 550, exit_img, exit_hover)

# Tower
tower = []

score_font = pygame.font.SysFont('LCDMono2', 60)

for i in range(1, 11):
    tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y - (30 * i),
                 240, 30, 1, color_manager.gradient_color()))

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

                    tower.append(Box(player.x, player.y, player.w,
                                 player.h, 0, player.color))

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
                        tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y -
                                     (30 * i), 240, 30, 1, color_manager.gradient_color()))

                    player = create_box(
                        0, 0, 240, 30, 4, color_manager.gradient_color())
                    player.y = tower[-1].y - 30
                    score = 0

        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BLACK)

    if status == "playing":
        player.draw()
        player.move()

    for box in tower:
        box.draw()

    text_surface = score_font.render(
        str(score), False, (255, 255, 255))
    screen.blit(text_surface, (SCREEN_X/2-text_surface.get_width()/2, 50))

    if retry_button.draw():
        # Reset the game
        status = "playing"
        tower = []

        for i in range(1, 11):
            tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y -
                             (30 * i), 240, 30, 1, color_manager.gradient_color()))

        player = create_box(
            0, 0, 240, 30, 4, color_manager.gradient_color())
        player.y = tower[-1].y - 30
        score = 0

    if exit_button.draw():
        pygame.quit()

    pygame.display.flip()
