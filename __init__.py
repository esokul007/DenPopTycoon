import pygame
import sys
import time

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DenPop Tycoon")
clock = pygame.time.Clock()

#Constants
FILL_SPEED = 0.1
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
# menu attributes
font_title = pygame.font.SysFont("Arial", 12, bold=True)
font_content = pygame.font.SysFont("Arial", 10)
menu_bg_color = (50, 50, 50)
menu_text_color = (255, 255, 255)

drink_recipes = {
    "All American Marching Band": {
        "powerade": 0.25,
        "sprite": 0.25,
        "lemonade": 0.25,
        "mountain dew": 0.25
    },
    "BirdDog": {
        "mountain dew": 0.5,
        "fanta": 0.25,
        "coke": 0.125,
        "mug": 0.125
    },
    "Blast of Baja": {
        "powerade": 0.25,
        "mountain dew": 0.75
    },
    "Bonecrush City": {
        "fanta": 0.666,
        "sprite": 0.333,
    },
    "Bug Juice": {
        "mountain dew": 0.333,
        "powerade": 0.2,
        "sprite": 0.6
    },
    "Candy Land": {
        "mug": 0.333,
        "fanta": 0.333,
        "mountain dew": 0.333
    },
    "Cherry Smuggler": {
        "coke": 0.5,
        "mountain dew": 0.5
    },
    "Citrus Slam!": {
        "sprite": 0.5,
        "mountain dew": 0.5
    },
    "Communist Threat": {
        "mug": 0.5,
        "coke": 0.5
    },
    "Cotton Candy Overdose": {
        "mug": 0.75,
        "powerade": 0.25
    },
    "The Boiler Babe": {
        "lemonade": 0.333,
        "fanta": 0.333,
        "mountain dew": 0.333
    },
    "Tooty Fruity": {
        "coke": 0.25,
        "mountain dew": 0.25,
        "powerade": 0.25,
        "lemonade": 0.25
    },
    "The IU Special": {
        "powerade": 0.5,
        "milk": 0.5,
    },
    "The Gynecologist": {
        "dr pepper": 0.333,
        "mug": 0.333,
        "coke": 0.333
    },
    "Dr Love": {
        "fanta": 0.5,
        "coke": 0.25,
        "mug": 0.25
    },
    "Dirty Sprite": {
        "water": 0.5,
        "sprite": 0.333,
        "lemonade": 0.166
    }
}

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

def draw_drink_menu(drink_name, ingredients, position):
    menu_width = 100
    menu_height = 30 + 12 * len(ingredients)
    x, y = position

    pygame.draw.rect(screen, menu_bg_color, (x, y, menu_width, menu_height), border_radius=4)

    title_surface = font_title.render(drink_name, True, menu_text_color)
    screen.blit(title_surface, (x + 5, y + 5))

    line_y = y + 20
    for ingredient, amount in ingredients.items():
        if isinstance(amount, float):
            text = f"{ingredient}: {amount:.2f}"
        else:
            text = f"{ingredient}: {amount}"
        content_surface = font_content.render(text, True, menu_text_color)
        screen.blit(content_surface, (x + 5, line_y))
        line_y += 12

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
                if sum(cup_contents.values()) >= 0.98:
                    print("Cup is full!")
                    continue
                else:
                    print({cup_contents[f"{name}"]})
                    cup_contents[f"{name}"] += FILL_SPEED
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

    # Draw all drink menus horizontally
    x_start, y_start = 10, 10
    x, y = x_start, y_start

    for drink_name, ingredients in drink_recipes.items():
        draw_drink_menu(drink_name, ingredients, (x, y))
        x += 80  # Space between menus

        # Optional: wrap to next row if off-screen
        if x > WIDTH - 80:
            x = x_start
            y += 60


    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second


