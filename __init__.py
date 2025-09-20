import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DenPop Tycoon")
clock = pygame.time.Clock()

#Constants
SODA_ICON_SIZE = (35,35)
SODA_ICON_Y = 275
SODA_ICON_START_X = 45
SODA_ICON_SPACING = 35

# Initial position of the cup
cup_x, cup_y = 350, 225
cup_contents= {"fanta": 0.0,
               "coke": 0.0,
               "lemonade": 0.0,
               "powerade": 0.0,
               "mug": 0.0,
               }
import time

dragging = False
offset_x, offset_y = 0, 0
cup_width = 40
cup_height = 60

# Define clickable areas under each soda icon
soda_buttons = {
    "coke": pygame.Rect(60, 345, 15, 20),
    "fanta": pygame.Rect(94, 345, 15, 20),
    "lemonade": pygame.Rect(128, 345, 15, 20),
    "mug": pygame.Rect(162, 345, 15, 20),
    "powerade": pygame.Rect(196, 345, 15, 20),
}

# Track last time each soda was filled
last_fill_time = {name: 0 for name in soda_buttons}

#image loading
counter = pygame.transform.scale(pygame.image.load("assets/counter.png"), (600, 250))
fountain = pygame.transform.scale(pygame.image.load("assets/fountain_pix.png"), (400, 250))

coke = pygame.transform.scale(pygame.image.load("assets/coke.jpg"), SODA_ICON_SIZE)
fanta = pygame.transform.scale(pygame.image.load("assets/fanta.jpg"), SODA_ICON_SIZE)
lemonade = pygame.transform.scale(pygame.image.load("assets/lemonade.jpg"), SODA_ICON_SIZE)
mug = pygame.transform.scale(pygame.image.load("assets/mug.jpg"), SODA_ICON_SIZE)
powerade = pygame.transform.scale(pygame.image.load("assets/powerade.jpg"), SODA_ICON_SIZE)

def draw_trapezoid_cup(x, y):
    # Define trapezoid points for upside-down cup
    top_width = cup_width
    bottom_width = 3/5 * cup_width
    height = cup_height
    points = [
        (x + (top_width - bottom_width) // 2, y + height),         # Bottom-left (narrow)
        (x + (top_width + bottom_width) // 2, y + height),         # Bottom-right (narrow)
        (x + top_width, y),                                        # Top-right (wide)
        (x, y)                                                     # Top-left (wide)
    ]
    # Draw semi-transparent trapezoid
    cup_surface = pygame.Surface((top_width, height), pygame.SRCALPHA)
    pygame.draw.polygon(cup_surface, (200, 200, 255, 150), [(p[0] - x, p[1] - y) for p in points])
    screen.blit(cup_surface, (x, y))

def draw_soda_icons():
    screen.blit(coke, (SODA_ICON_START_X, SODA_ICON_Y))
    screen.blit(fanta, (SODA_ICON_START_X+ SODA_ICON_SPACING, SODA_ICON_Y))
    screen.blit(lemonade, (SODA_ICON_START_X+ 2*SODA_ICON_SPACING, SODA_ICON_Y))
    screen.blit(mug, (SODA_ICON_START_X+ 3*SODA_ICON_SPACING, SODA_ICON_Y))
    screen.blit(powerade, (SODA_ICON_START_X+ 4*SODA_ICON_SPACING, SODA_ICON_Y))

    # Draw gray rectangles (buttons) under each icon
    for rect in soda_buttons.values():
        pygame.draw.rect(screen, (100, 100, 100), rect)

while True:
    cup_rect = pygame.Rect(cup_x, cup_y, cup_width, cup_height)  # Adjust to match your cup size
    current_time = time.time()
    for name, rect in soda_buttons.items():
        if current_time - last_fill_time[name] >= 1.0:
            if cup_rect.colliderect(rect):
                print({cup_contents[f"{name}"]})
                cup_contents[f"{name}"] += 0.02
                last_fill_time[name] = current_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
           # Simple bounding box check
            if cup_x <= mouse_x <= cup_x + 100 and cup_y <= mouse_y <= cup_y + 150:
                dragging = True
                offset_x = cup_x - mouse_x
                offset_y = cup_y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                cup_rect = pygame.Rect(cup_x, cup_y, cup_width, cup_height)  # Adjust to match your cup size
                mouse_x, mouse_y = event.pos
                cup_x = mouse_x + offset_x
                cup_y = mouse_y + offset_y
                
                        

    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(counter, (0, 430))
    screen.blit(fountain, (40, 230))
    draw_soda_icons()
    draw_trapezoid_cup(cup_x, cup_y)

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second


