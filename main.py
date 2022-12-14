import pygame
from random import choice


class Box:
    def __init__(self, x: int, y: int, w: int, h: int, speed: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed

    def draw(self) -> None:
        """Draws the box on the screen"""
        # Wrapped values in int() to fix a bug
        self.image = pygame.transform.scale(brick_img, (int(self.w), int(self.h)))
        screen.blit(self.image, (int(self.x), int(self.y)))

    def move(self) -> None:
        """Moves the box"""
        left = self.x
        right = self.x + self.w

        if left < 0 or right > SCREEN_X:
            self.speed *= -1

            bounce_sound.play()

        self.x += self.speed


class Button:
    def __init__(self, x: int, y: int, image: pygame.Surface, hover_image: pygame.Surface) -> None:
        # Scale the images
        self.image = pygame.transform.scale(image, (int(image.get_width() * 0.6), int(image.get_height() * 0.6)))
        self.hover = pygame.transform.scale(hover_image, (int(hover_image.get_width() * 0.6), int(hover_image.get_height() * 0.6)))
        # Position the images
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pressed = False

    def draw(self) -> bool:
        """Draws the button, returns True if it has been pressed"""
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


def create_box(x: int, y: int, w: int, h: int, speed: int) -> Box:
    """Generates a box object"""
    return Box(x, SCREEN_Y - 50 - y, w, h, speed)


def happy() -> None:
    """Plays happy music"""
    pygame.mixer.music.load("audio/happy.wav")
    pygame.mixer.music.play(-1)
    pygame.display.set_icon(pygame.image.load("images/happy_icon.png"))
    pygame.display.set_caption("stack game but python :D")


def suspense() -> None:
    """Plays suspensful music"""
    pygame.mixer.music.load("audio/suspense.wav")
    pygame.mixer.music.play(-1)
    pygame.display.set_icon(pygame.image.load("images/suspense_icon.png"))
    pygame.display.set_caption("stack game but python :C")


# Set constant variables
SCREEN_X = 480
SCREEN_Y = 640
RESOLUTION = (SCREEN_X, SCREEN_Y)
FPS = 120

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Sound
pygame.mixer.music.set_volume(0.25)
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("pystack")
clock = pygame.time.Clock()  # Sync FPS
pygame.display.set_icon(pygame.image.load("images/suspense_icon.png"))  # Use custom icon

# Load sound effects
place_sound = pygame.mixer.Sound("audio/place.wav")
place_sound.set_volume(0.25)
loss_sound = pygame.mixer.Sound("audio/loss.wav")
loss_sound.set_volume(0.25)
bounce_sound = pygame.mixer.Sound("audio/bounce.wav")
bounce_sound.set_volume(0.25)
god_mode_sound_on = pygame.mixer.Sound("audio/god_mode_on.wav")
god_mode_sound_on.set_volume(0.25)
god_mode_sound_off = pygame.mixer.Sound("audio/god_mode_off.wav")
god_mode_sound_off.set_volume(0.25)

# Load images
brick_img = pygame.image.load("images/brick.jpg").convert()

retry_img = pygame.image.load("images/retry.png").convert_alpha()
retry_hover = pygame.image.load("images/retry_hover.png").convert_alpha()

exit_img = pygame.image.load("images/quit.png").convert_alpha()
exit_hover = pygame.image.load("images/quit_hover.png").convert_alpha()

bg_img = pygame.image.load("images/background.jpg").convert()
bg_y = -640 * 2  # Offset for the background image

# Create buttons
retry_button = Button(50, 550, retry_img, retry_hover)
exit_button = Button(250, 550, exit_img, exit_hover)

# Tower setup
tower = []

for i in range(1, 11):
    tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y - (30 * i), 240, 30, 1))


# Text setup
score_font = pygame.font.Font("fonts/LCDMono2.ttf", 60)
fps_font = pygame.font.Font("fonts/LCDMono2.ttf", 20)

# Score and game state
score = 0
status = "playing"

# Player setup
player = create_box(0, 0, 240, 30, 2)
player.y = tower[-1].y - 30

# God mode easter egg / debug, activate by pressing 'G'
god_mode = False

print("Game started\nPress G for god mode")

suspense()

# Game loop
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 103:
                god_mode = not god_mode
                print("God mode: " + str(god_mode) + " \U0001F607") if god_mode else print("God mode: " + str(god_mode) + " \U0001F62D")
                if god_mode:
                    god_mode_sound_on.play()
                    happy()
                else:
                    god_mode_sound_off.play()
                    suspense()
            if event.key == 32:
                if status == "playing":
                    last_box = tower[-1]

                    # Variables for easier reading
                    current_left = player.x
                    current_right = player.x + player.w

                    last_left = last_box.x
                    last_right = last_box.x + last_box.w

                    if not god_mode:
                        # Overlap left
                        if current_left < last_left:
                            player.x = last_box.x
                            player.w -= last_right - current_right
                        # Overlap right
                        elif current_right > last_right:
                            player.w -= current_right - last_right

                    if player.w <= 1:
                        status = "lost"
                        loss_sound.play()
                    else:
                        place_sound.play()

                        tower.append(Box(player.x, player.y, player.w, player.h, 0))

                        # Move all boxes down to create the illusion of a stack
                        for box in tower:
                            box.y += 30
                        else:
                            bg_y += 30

                        # Move the player to the left or right side of the screen
                        player.x = choice([0, SCREEN_X - player.w])

                        # Set the speed to the correct direction so the box doesn't bounce the instant it spawns
                        if player.x == 0:
                            player.speed = 2 + (score / 10)
                        elif player.x == SCREEN_X - player.w:
                            player.speed = -2 - (score / 10)

                        score += 1

        if event.type == pygame.QUIT:
            pygame.quit()

    # Draw the background
    screen.fill((0, 0, 0))
    screen.blit(bg_img, (0, bg_y))

    # Draw the score
    text_surface = score_font.render(str(score), True, (255, 255, 255))
    screen.blit(text_surface, (SCREEN_X / 2 - text_surface.get_width() / 2, 50))

    # Draw FPS
    fps_text = fps_font.render("FPS: " + str(int(clock.get_fps())), True, (255, 255, 255))
    screen.blit(fps_text, (SCREEN_X - fps_text.get_width() - 10, 10))

    if status == "playing":
        player.draw()
        player.move()

    for box in tower:
        box.draw()

    if status == "lost":
        if retry_button.draw():
            # Reset the game
            status = "playing"
            tower = []

            for i in range(1, 11):
                tower.append(Box((SCREEN_X / 2) - 120, SCREEN_Y - (30 * i), 240, 30, 1))

            player = create_box(0, 0, 240, 30, 2)
            player.y = tower[-1].y - 30
            bg_y = -640 * 2
            score = 0

        if exit_button.draw():
            pygame.quit()

    pygame.display.flip()
