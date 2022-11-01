import pygame


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

# Initialize pygame and create window
pygame.init()
pygame.mixer.init()  # Sound
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("pyStack")
clock = pygame.time.Clock()  # Sync FPS

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(BLACK)

    ########################
    #### Your code here ####
    ########################

    pygame.display.flip()
