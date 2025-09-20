import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DenPop Tycoon")
clock = pygame.time.Clock()

#Constants
SODA_ICON_SIZE = (35,35)
SODA_ICON_Y = 450git
SODA_ICON_START_X = 45
SODA_ICON_SPACING = 35




#image loading
counter = pygame.transform.scale(pygame.image.load("assets/counter.png"), (600, 250))
fountain = pygame.transform.scale(pygame.image.load("assets/fountain_pix.png"), (400, 250))

coke = pygame.transform.scale(pygame.image.load("assets/coke.jpg"), SODA_ICON_SIZE)
fanta = pygame.transform.scale(pygame.image.load("assets/fanta.jpg"), SODA_ICON_SIZE)
lemonade = pygame.transform.scale(pygame.image.load("assets/lemonade.jpg"), SODA_ICON_SIZE)
mug = pygame.transform.scale(pygame.image.load("assets/mug.jpg"), SODA_ICON_SIZE)
powerade = pygame.transform.scale(pygame.image.load("assets/powerade.jpg"), SODA_ICON_SIZE)


def draw_soda_icons():
    screen.blit(coke, (SODA_ICON_START_X, SODA_ICON_Y))
    screen.blit(fanta, (SODA_ICON_START_X+ SODA_ICON_SPACING, SODA_ICON_Y))
    screen.blit(lemonade, (SODA_ICON_START_X+ 2*SODA_ICON_SPACING, SODA_ICON_Y))
    screen.blit(mug, (SODA_ICON_START_X+ 3*SODA_ICON_SPACING, SODA_ICON_Y))
    screen.blit(powerade, (SODA_ICON_START_X+ 4*SODA_ICON_SPACING, SODA_ICON_Y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(counter, (0, 430))
    screen.blit(fountain, (40, 230))
    
    draw_soda_icons()
    
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

