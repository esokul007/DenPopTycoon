from __future__ import annotations
import random
import sys
import time
import pygame
import math
from pygame.math import Vector2

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
COUNTER_POSITION = (0, 430)
FOUNTAIN_POSITION = (40, 230)
SCOREBOARD_POSITION = (700, 100)
COUNTER_SIZE = (600, 250)
FOUNTAIN_SIZE = (400, 250)

ORDER_POSITION = (620, 350)
CUSTOMER_SPAWN_POSITION = (600, 400)
CUSTOMER_SIZE = (200, 200)
customer_wait_time = 30  # seconds
TIME_MULTIPLIER = 0.9

# Timer attributes
    # Timer bar dimensions
TIME_BAR_X = 200
TIME_BAR_Y = 50
TIME_BAR_WIDTH = 450  # total width of the timer bar
TIME_BAR_HEIGHT = 30

CUP_WIDTH = 40
CUP_HEIGHT = 60
START_CUP_POSITION = (480, 415)

FILL_SPEED = 0.02
FILL_COOLDOWN_SECONDS = 0.1
MAX_FILL_LEVEL = 0.98

SODA_ICON_SIZE = (35, 35)
SODA_ICON_Y = 275
SODA_ICON_START_X = 47
SODA_ICON_SPACING = 34

SODA_BUTTONS = {
    "coke": pygame.Rect(60, 345, 15, 20),
    "fanta": pygame.Rect(93, 345, 15, 20),
    "lemonade": pygame.Rect(128, 345, 15, 20),
    "mug": pygame.Rect(162, 345, 15, 20),
    "powerade": pygame.Rect(195, 345, 15, 20),
    "mountain_dew": pygame.Rect(228, 345, 15, 20),
    "sprite": pygame.Rect(262, 345, 15, 20),
    "water": pygame.Rect(296, 345, 15, 20),
    "milk": pygame.Rect(330, 345, 15, 20),
}

SODA_ICON_FILES = {
    "coke": "assets/coke.jpg",
    "fanta": "assets/fanta.jpg",
    "lemonade": "assets/lemonade.jpg",
    "mug": "assets/mug.jpg",
    "powerade": "assets/powerade.jpg",
    "mountain_dew": "assets/mountain_dew.png",
    "sprite": "assets/sprite.jpg",
    "water": "assets/water.png",
    "milk": "assets/milk.jpg",
}

SELL_SOUND = pygame.mixer.Sound("assets/ChaChing.mp3")

SODA_RGB_COLORS = {
    "coke": (91, 18, 18),
    "fanta": (255, 145, 0),
    "lemonade": (231, 235, 117),
    "mug": (87, 58, 9),
    "powerade": (26, 160, 249),
    "mountain_dew": (185, 253, 170),
    "sprite": (211, 173, 242),
    "water": (211, 246, 242),
    "milk": (255, 255, 255),
}

CUSTOMER_ICON_FILES = {
    "customer1": "assets/guy1.png",
    "customer2": "assets/guy2.png",
    "customer3": "assets/purdue_pete.png"
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
DRINK_NAMES = list(DRINK_RECIPES.keys())

FONT_TITLE = pygame.font.SysFont("Arial", 12, bold=True)
FONT_CONTENT = pygame.font.SysFont("Arial", 10)
MENU_BG_COLOR = (241, 239, 208)
MENU_TEXT_COLOR = (0, 0, 0)

ORDER_FONT = pygame.font.SysFont("Arial", 16)
BUBBLE_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
BORDER_COLOR = (0, 0, 0)

menu_index = 0
menu_display = True

score = 0

class Customer:
    def __init__(self) -> None:
        global customer_wait_time
        self.order = random.choice(list(DRINK_RECIPES.keys()))
        base_image = pygame.image.load(random.choice(list(CUSTOMER_ICON_FILES.values())))
        self.base_sprite = pygame.transform.scale(base_image, CUSTOMER_SIZE)
        self.mask = pygame.mask.from_surface(self.base_sprite)
        self.status = "waiting"  # could be 'waiting', 'served', 'left'
        self.wait_time = customer_wait_time
        self.max_changes = 1

    def update(self, dt: float) -> None:
        if self.status != "waiting":
            return
        self.wait_time = max(0.0, self.wait_time - dt)
        if self.wait_time <= 0:
            self.wait_time = 0.0
            self.status = "left"

    def get_tinted_sprite(self) -> pygame.Surface:
        global customer_wait_time
        if self.status != "waiting":
            return self.base_sprite
        remaining_ratio = max(0.0, min(1.0, self.wait_time / customer_wait_time))
        impatience = 1.0 - remaining_ratio
        if impatience <= 0:
            return self.base_sprite
        tinted = self.base_sprite.copy()
        red_amount = int(255 * impatience)
        overlay_surface = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        overlay = self.mask.to_surface(overlay_surface, setcolor=(red_amount, 0, 0, 0), unsetcolor=(0, 0, 0, 0))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted

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
    
    def calculate_color(self) -> tuple[int, int, int]:
        r = g = b = 0
        total = self.fill_level
        if total == 0:
            return (255, 255, 255)  # Empty cup is white
        for soda, amount in self.contents.items():
            ratio = amount / total
            sr, sg, sb = SODA_RGB_COLORS.get(soda, (255, 255, 255))
            r += sr * ratio
            g += sg * ratio
            b += sb * ratio
        return (int(r), int(g), int(b))
    
# Three below methods are used for calculating order correctness
def normalize(d):
    total = sum(d.values())
    return {k: v / total for k, v in d.items()} if total > 0 else d

def cosine_similarity(a, b):
    keys = set(a.keys()) | set(b.keys())
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    mag_a = math.sqrt(sum(a.get(k, 0)**2 for k in keys))
    mag_b = math.sqrt(sum(b.get(k, 0)**2 for k in keys))
    return dot / (mag_a * mag_b) if mag_a and mag_b else 0

def calc_score(cup, order):
    normalized_cup = normalize(cup)
    normalized_order = DRINK_RECIPES[order]
    similarity = cosine_similarity(normalized_cup, normalized_order)
    if (similarity*100) < 30:
        return -50
    return (similarity * 100)  # Scale to 0-100

def load_static_images() -> dict[str, pygame.Surface]:
    return {
        "counter": pygame.transform.scale(pygame.image.load("assets/counter.png"), COUNTER_SIZE),
        "fountain": pygame.transform.scale(pygame.image.load("assets/fountain_pix.png"), FOUNTAIN_SIZE),
        "background": pygame.transform.scale(pygame.image.load("assets/background.png"), SCREEN_SIZE),
    }


def load_soda_icons() -> dict[str, pygame.Surface]:
    return {
        name: pygame.transform.scale(pygame.image.load(path), SODA_ICON_SIZE)
        for name, path in SODA_ICON_FILES.items()
    }

def draw_text_bubble(screen: pygame.Surface, text, position):
    padding = 10
    x, y = position

    # Render text
    text_surface = ORDER_FONT.render(text, True, TEXT_COLOR)
    text_width, text_height = text_surface.get_size()

    # Bubble dimensions
    bubble_width = text_width + padding * 2
    bubble_height = text_height + padding * 2

    # Draw bubble background
    pygame.draw.rect(screen, BUBBLE_COLOR, (x, y, bubble_width, bubble_height), border_radius=8)

    # Optional: draw border
    pygame.draw.rect(screen, BORDER_COLOR, (x, y, bubble_width, bubble_height), 2, border_radius=8)

    # Blit text
    screen.blit(text_surface, (x + padding, y + padding))


def draw_drink_menu(
    screen: pygame.Surface,
    drink_name: str,
    ingredients: dict[str, float],
    position: tuple[int, int],
) -> None:
    menu_width = 140
    menu_height = 60 + 12 * len(ingredients)
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

    # Calculate fill height
    fill_level = min(cup.fill_level, 1.0)
    fill_height = int(height * fill_level)
    fill_y = y + height - fill_height

    # Calculate fill trapezoid width at current height
    width_diff = top_width - bottom_width
    current_width = bottom_width + int(width_diff * (fill_height / height))

    # Center the fill trapezoid horizontally
    fill_x = x + (top_width - current_width) // 2

    # Fill trapezoid points
    fill_bottom_left = (x + (top_width - bottom_width) // 2, y + height)
    fill_bottom_right = (x + (top_width + bottom_width) // 2, y + height)
    fill_top_left = (fill_x, fill_y)
    fill_top_right = (fill_x + current_width, fill_y)

    fill_points = [fill_bottom_left, fill_bottom_right, fill_top_right, fill_top_left]
    pygame.draw.polygon(screen, cup.calculate_color(), fill_points)

    # Draw cup outline
    cup_points = [
        (x + (top_width - bottom_width) // 2, y + height),
        (x + (top_width + bottom_width) // 2, y + height),
        (x + top_width, y),
        (x, y),
    ]
    cup_surface = pygame.Surface((top_width, height), pygame.SRCALPHA)
    pygame.draw.polygon(cup_surface, (200, 200, 255, 80), [(px - x, py - y) for px, py in cup_points])
    screen.blit(cup_surface, (x, y))


def draw_soda_icons(screen: pygame.Surface, icons: dict[str, pygame.Surface]) -> None:
    x = SODA_ICON_START_X
    for name in SODA_BUTTONS:
        screen.blit(icons[name], (x, SODA_ICON_Y))
        x += SODA_ICON_SPACING

    for button in SODA_BUTTONS.values():
        pygame.draw.rect(screen, (100, 100, 100), button)

def draw_customer(screen: pygame.Surface, customer: Customer, position: tuple[int, int]) -> None:
    screen.blit(customer.get_tinted_sprite(), position)

def draw_timer(screen: pygame.Surface, customer: Customer):

    # Draw background bar
    pygame.draw.rect(screen, (255, 255, 255), (TIME_BAR_X, TIME_BAR_Y, TIME_BAR_WIDTH, TIME_BAR_HEIGHT))

    # Calculate fill width based on remaining time
    fill_ratio = max(0.0, min(customer.wait_time / customer_wait_time, 1.0))
    fill_width = int(TIME_BAR_WIDTH * fill_ratio)

    # Draw fill bar
    pygame.draw.rect(screen, (0, 255, 0), (TIME_BAR_X, TIME_BAR_Y, fill_width, TIME_BAR_HEIGHT))

def random_order_change(screen: pygame.Surface, customer: Customer) -> None:
    global customer_wait_time
    ratio = customer.wait_time / customer_wait_time
    if (0.7 <= ratio <= 0.8) and customer.max_changes == 1:
        if random.random() < 0.2:  # 20% chance if timer is between 70% and 80% done. Only 1 change should be made if any.
            customer.order = random.choice(list(DRINK_RECIPES.keys()))
            print(f"Customer changed order to {customer.order}")
        customer.max_changes = 0


def draw_score(screen: pygame.Surface) -> None:
    score_surface = ORDER_FONT.render(f"Score: {score:.0f}", True, (255, 255, 255))
    screen.blit(score_surface, SCOREBOARD_POSITION)

def draw_frame(
    screen: pygame.Surface,
    static_images: dict[str, pygame.Surface],
    soda_icons: dict[str, pygame.Surface],
    customer: Customer,
    cup: Cup,
) -> None:
    screen.blit(static_images["background"], (0, 0))
    screen.blit(static_images["counter"], COUNTER_POSITION)
    screen.blit(static_images["fountain"], FOUNTAIN_POSITION)
    draw_soda_icons(screen, soda_icons)
    if customer.status == "waiting":
        draw_customer(screen, customer, CUSTOMER_SPAWN_POSITION)
        draw_text_bubble(screen, customer.order, ORDER_POSITION)
    draw_trapezoid_cup(screen, cup)

    drink_name = DRINK_NAMES[menu_index]
    ingredients = DRINK_RECIPES[drink_name]
    global menu_display
    if menu_display:
        draw_drink_menu(screen, drink_name, ingredients, (50, 50))
    draw_score(screen)
    draw_timer(screen, customer)
    random_order_change(screen, customer)


def handle_events(cup: Cup, customer: Customer) -> bool:
    global score, menu_display
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and cup.rect.collidepoint(event.pos):
            cup.start_drag(event.pos)
            menu_display = False # display menu off if cup clicked
        elif event.type == pygame.MOUSEBUTTONUP:
            cup.stop_drag()
            menu_display = True
        elif event.type == pygame.MOUSEMOTION:
            cup.drag(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SELL_SOUND.play()
                customer.status = "served" # serve order
                score = max((score + calc_score(cup.contents, customer.order)), 0) # 
                cup.contents = {name: 0.0 for name in SODA_BUTTONS} # reset cup
            if event.key == pygame.K_q:
                cup.contents = {name: 0.0 for name in SODA_BUTTONS} # reset cup
            if event.key == pygame.K_RIGHT:
                global menu_index
                menu_index =(menu_index + 1) % len(DRINK_NAMES)
                cup.stop_drag()
                cup.position = Vector2(*START_CUP_POSITION) # reset cup position
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
    previous_time = time.time()

    while True:
        now = time.time()
        dt = now - previous_time
        previous_time = now
        if not handle_events(cup, customer):
            break
        customer.update(dt)
        if customer.status in {"served", "left"}:
            if customer.status == "left":
                global score
                score -= 50
                print("Customer left before being served.")
            global customer_wait_time
            customer_wait_time = max((customer_wait_time * TIME_MULTIPLIER), 20) # Faster order time. Min 20 seconds.
            customer = Customer()
            print(f"Customer order: {customer.order}")
            previous_time = now
        update_cup_fill(cup, last_fill_time, now)
        draw_frame(screen, static_images, soda_icons, customer, cup)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()











