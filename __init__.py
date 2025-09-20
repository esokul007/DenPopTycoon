from __future__ import annotations
import random
import sys
import time
import pygame
from pygame.math import Vector2

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
COUNTER_POSITION = (0, 430)
FOUNTAIN_POSITION = (40, 230)
COUNTER_SIZE = (600, 250)
FOUNTAIN_SIZE = (400, 250)

CUSTOMER_SPAWN_POSITION = (600, 400)
CUSTOMER_SIZE = (200, 200)

CUP_WIDTH = 40
CUP_HEIGHT = 60
START_CUP_POSITION = (350, 225)

FILL_SPEED = 0.1
FILL_COOLDOWN_SECONDS = 1.0
MAX_FILL_LEVEL = 0.98

SODA_ICON_SIZE = (35, 35)
SODA_ICON_Y = 275
SODA_ICON_START_X = 45
SODA_ICON_SPACING = 35

SODA_BUTTONS = {
    "coke": pygame.Rect(60, 345, 15, 20),
    "fanta": pygame.Rect(94, 345, 15, 20),
    "lemonade": pygame.Rect(128, 345, 15, 20),
    "mug": pygame.Rect(162, 345, 15, 20),
    "powerade": pygame.Rect(196, 345, 15, 20),
}

SODA_ICON_FILES = {
    "coke": "assets/coke.jpg",
    "fanta": "assets/fanta.jpg",
    "lemonade": "assets/lemonade.jpg",
    "mug": "assets/mug.jpg",
    "powerade": "assets/powerade.jpg",
}

CUSTOMER_ICON_FILES = {
    "customer1": "assets/guy1.png",
    "customer2": "assets/guy2.png",
}

DRINK_RECIPES = {
    "All American Marching Band": {
        "powerade": 0.25,
        "sprite": 0.25,
        "lemonade": 0.25,
        "mountain dew": 0.25,
    },
    "BirdDog": {
        "mountain dew": 0.5,
        "fanta": 0.25,
        "coke": 0.125,
        "mug": 0.125,
    },
    "Blast of Baja": {
        "powerade": 0.25,
        "mountain dew": 0.75,
    },
    "Bonecrush City": {
        "fanta": 0.666,
        "sprite": 0.333,
    },
    "Bug Juice": {
        "mountain dew": 0.333,
        "powerade": 0.2,
        "sprite": 0.6,
    },
    "Candy Land": {
        "mug": 0.333,
        "fanta": 0.333,
        "mountain dew": 0.333,
    },
    "Cherry Smuggler": {
        "coke": 0.5,
        "mountain dew": 0.5,
    },
    "Citrus Slam!": {
        "sprite": 0.5,
        "mountain dew": 0.5,
    },
    "Communist Threat": {
        "mug": 0.5,
        "coke": 0.5,
    },
    "Cotton Candy Overdose": {
        "mug": 0.75,
        "powerade": 0.25,
    },
    "The Boiler Babe": {
        "lemonade": 0.333,
        "fanta": 0.333,
        "mountain dew": 0.333,
    },
    "Tooty Fruity": {
        "coke": 0.25,
        "mountain dew": 0.25,
        "powerade": 0.25,
        "lemonade": 0.25,
    },
    "The IU Special": {
        "powerade": 0.5,
        "milk": 0.5,
    },
    "The Gynecologist": {
        "dr pepper": 0.333,
        "mug": 0.333,
        "coke": 0.333,
    },
    "Dr Love": {
        "fanta": 0.5,
        "coke": 0.25,
        "mug": 0.25,
    },
    "Dirty Sprite": {
        "water": 0.5,
        "sprite": 0.333,
        "lemonade": 0.166,
    },
}

FONT_TITLE = pygame.font.SysFont("Arial", 12, bold=True)
FONT_CONTENT = pygame.font.SysFont("Arial", 10)
MENU_BG_COLOR = (50, 50, 50)
MENU_TEXT_COLOR = (255, 255, 255)

class Customer:
    def __init__(self) -> None:
        self.order = random.choice(list(DRINK_RECIPES.keys()))
        self.sprite = pygame.transform.scale(pygame.image.load(random.choice(list(CUSTOMER_ICON_FILES.values()))), CUSTOMER_SIZE)
        self.status = "waiting"  # could be 'waiting', 'served', 'left'


class Cup:
    def __init__(self, x: int, y: int) -> None:
        self.position = Vector2(x, y)
        self.offset = Vector2()
        self.dragging = False
        self.contents = {name: 0.0 for name in SODA_BUTTONS}

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), CUP_WIDTH, CUP_HEIGHT)

    @property
    def fill_level(self) -> float:
        return sum(self.contents.values())

    @property
    def is_full(self) -> bool:
        return self.fill_level >= MAX_FILL_LEVEL

    def start_drag(self, mouse_pos: tuple[int, int]) -> None:
        self.dragging = True
        self.offset = self.position - Vector2(mouse_pos)

    def drag(self, mouse_pos: tuple[int, int]) -> None:
        if not self.dragging:
            return
        self.position = Vector2(mouse_pos) + self.offset

    def stop_drag(self) -> None:
        self.dragging = False

    def fill(self, soda_name: str, amount: float) -> bool:
        if soda_name not in self.contents or self.is_full:
            return False
        self.contents[soda_name] = min(1.0, self.contents[soda_name] + amount)
        return True


def load_static_images() -> dict[str, pygame.Surface]:
    return {
        "counter": pygame.transform.scale(pygame.image.load("assets/counter.png"), COUNTER_SIZE),
        "fountain": pygame.transform.scale(pygame.image.load("assets/fountain_pix.png"), FOUNTAIN_SIZE),
    }


def load_soda_icons() -> dict[str, pygame.Surface]:
    return {
        name: pygame.transform.scale(pygame.image.load(path), SODA_ICON_SIZE)
        for name, path in SODA_ICON_FILES.items()
    }


def draw_drink_menu(
    screen: pygame.Surface,
    drink_name: str,
    ingredients: dict[str, float],
    position: tuple[int, int],
) -> None:
    menu_width = 100
    menu_height = 30 + 12 * len(ingredients)
    x, y = position

    pygame.draw.rect(screen, MENU_BG_COLOR, (x, y, menu_width, menu_height), border_radius=4)

    title_surface = FONT_TITLE.render(drink_name, True, MENU_TEXT_COLOR)
    screen.blit(title_surface, (x + 5, y + 5))

    line_y = y + 20
    for ingredient, amount in ingredients.items():
        label = f"{ingredient}: {amount:.2f}" if isinstance(amount, float) else f"{ingredient}: {amount}"
        content_surface = FONT_CONTENT.render(label, True, MENU_TEXT_COLOR)
        screen.blit(content_surface, (x + 5, line_y))
        line_y += 12


def draw_trapezoid_cup(screen: pygame.Surface, cup: Cup) -> None:
    x = int(cup.position.x)
    y = int(cup.position.y)
    top_width = CUP_WIDTH
    bottom_width = int(0.6 * CUP_WIDTH)
    height = CUP_HEIGHT

    points = [
        (x + (top_width - bottom_width) // 2, y + height),
        (x + (top_width + bottom_width) // 2, y + height),
        (x + top_width, y),
        (x, y),
    ]

    cup_surface = pygame.Surface((top_width, height), pygame.SRCALPHA)
    pygame.draw.polygon(cup_surface, (200, 200, 255, 150), [(px - x, py - y) for px, py in points])
    screen.blit(cup_surface, (x, y))


def draw_soda_icons(screen: pygame.Surface, icons: dict[str, pygame.Surface]) -> None:
    x = SODA_ICON_START_X
    for name in SODA_BUTTONS:
        screen.blit(icons[name], (x, SODA_ICON_Y))
        x += SODA_ICON_SPACING

    for button in SODA_BUTTONS.values():
        pygame.draw.rect(screen, (100, 100, 100), button)

def draw_customer(screen: pygame.Surface, customer: Customer, position: tuple[int, int]) -> None:
    screen.blit(customer.sprite, position)

def draw_drink_menus(screen: pygame.Surface) -> None:
    x, y = 10, 10
    for drink_name, ingredients in DRINK_RECIPES.items():
        draw_drink_menu(screen, drink_name, ingredients, (x, y))
        x += 80
        if x > SCREEN_WIDTH - 80:
            x = 10
            y += 60


def draw_frame(
    screen: pygame.Surface,
    static_images: dict[str, pygame.Surface],
    soda_icons: dict[str, pygame.Surface],
    customer: Customer,
    cup: Cup,
) -> None:
    screen.fill(BACKGROUND_COLOR)
    screen.blit(static_images["counter"], COUNTER_POSITION)
    screen.blit(static_images["fountain"], FOUNTAIN_POSITION)
    draw_soda_icons(screen, soda_icons)
    draw_customer(screen, customer, CUSTOMER_SPAWN_POSITION)
    draw_trapezoid_cup(screen, cup)
    draw_drink_menus(screen)


def handle_events(cup: Cup) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and cup.rect.collidepoint(event.pos):
            cup.start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            cup.stop_drag()
        elif event.type == pygame.MOUSEMOTION:
            cup.drag(event.pos)
    return True


def update_cup_fill(cup: Cup, last_fill_time: dict[str, float], now: float) -> None:
    for soda_name, button in SODA_BUTTONS.items():
        if now - last_fill_time[soda_name] < FILL_COOLDOWN_SECONDS:
            continue
        if not cup.rect.colliderect(button):
            continue
        if cup.is_full:
            print("Cup is full!")
            continue
        if cup.fill(soda_name, FILL_SPEED):
            last_fill_time[soda_name] = now
            print(f"{soda_name}: {cup.contents[soda_name]:.2f}")


def main() -> None:
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("DenPop Tycoon")
    clock = pygame.time.Clock()

    static_images = load_static_images()
    soda_icons = load_soda_icons()
    cup = Cup(*START_CUP_POSITION)
    last_fill_time = {name: 0.0 for name in SODA_BUTTONS}
    
    # Create a customer and print their order
    customer = Customer()
    print(f"Customer order: {customer.order}")

    while True:
        now = time.time()
        if not handle_events(cup):
            break
        update_cup_fill(cup, last_fill_time, now)
        draw_frame(screen, static_images, soda_icons, customer, cup)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


