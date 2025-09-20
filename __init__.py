import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DenPop Tycoon")
clock = pygame.time.Clock()

#Constatns
SODA_ICON_SIZE = (35,35)




#image loading
counter = pygame.transform.scale(pygame.image.load("assets/counter.png"), (600, 250))
fountain = pygame.transform.scale(pygame.image.load("assets/fountain_pix.png"), (400, 250))

coke = pygame.transform.scale(pygame.image.load("assets/coke.jpg"), SODA_ICON_SIZE)
fanta = pygame.transform.scale(pygame.image.load("assets/fanta.jpg"), SODA_ICON_SIZE)
lemonade = pygame.transform.scale(pygame.image.load("assets/lemonade.jpg"), SODA_ICON_SIZE)
mug = pygame.transform.scale(pygame.image.load("assets/mug.jpg"), SODA_ICON_SIZE)
powerade = pygame.transform.scale(pygame.image.load("assets/powerade.jpg"), SODA_ICON_SIZE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(counter, (0, 430))
    screen.blit(fountain, (40, 230))
    screen.blit(coke, (45, 275))
    screen.blit(fanta, (80, 275))
    screen.blit(lemonade, (115, 275))
    screen.blit(mug, (150, 275))
    screen.blit(powerade, (185, 275))
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second
