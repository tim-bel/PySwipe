import pygame
import random
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE_GAUGE = 24
FONT_SIZE_CARD = 30
FONT_SIZE_GAMEOVER = 72

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (200, 200, 200)
COLOR_DARK_GREY = (50, 50, 50)
COLOR_ENERGY = (50, 200, 50)     # Green
COLOR_MONEY = (255, 215, 0)      # Gold
COLOR_TIME = (100, 149, 237)   # Cornflower Blue

# Game Parameters
GAUGE_MIN = 0
GAUGE_MAX = 100
GAUGE_INITIAL = 50

# --- Card Deck ---
# Each card has a text description and the effects for swiping right (agree) or left (deny).
CARDS = [
    {
        "text": "A dragon is attacking a nearby village! Intervene?",
        "right_effects": {"energy": -30, "money": 50, "time": -25},
        "left_effects": {"energy": -5, "money": -10, "time": -5},
    },
    {
        "text": "A shady merchant offers a 'shortcut' through the haunted forest.",
        "right_effects": {"energy": -10, "money": -15, "time": 25},
        "left_effects": {"energy": 0, "money": 0, "time": -15},
    },
    {
        "text": "The King requests an audience. He seems bored. Entertain him?",
        "right_effects": {"energy": -15, "money": 20, "time": -20},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
    },
    {
        "text": "You find a mysterious, glowing mushroom. Eat it?",
        "right_effects": {"energy": 40, "money": -5, "time": -5},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
    },
    {
        "text": "A traveling circus is in town. Spend the day watching shows?",
        "right_effects": {"energy": 20, "money": -20, "time": -25},
        "left_effects": {"energy": 5, "money": 0, "time": -5},
    },
    {
        "text": "Your rival challenges you to a duel at dawn.",
        "right_effects": {"energy": -25, "money": 25, "time": -10},
        "left_effects": {"energy": -10, "money": -10, "time": -5},
    },
    {
        "text": "A powerful wizard offers to enchant your gear for a hefty price.",
        "right_effects": {"energy": 10, "money": -40, "time": -15},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
    },
     {
        "text": "Spend all night at the tavern gambling and drinking?",
        "right_effects": {"energy": -20, "money": 35, "time": -20},
        "left_effects": {"energy": 10, "money": 0, "time": -5},
    },
]

# --- Setup Screen and Fonts ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Swipe Quest")
clock = pygame.time.Clock()

font_gauge = pygame.font.Font(None, FONT_SIZE_GAUGE)
font_card = pygame.font.Font(None, FONT_SIZE_CARD)
font_gameover = pygame.font.Font(None, FONT_SIZE_GAMEOVER)

# --- Game State Variables ---
energy = GAUGE_INITIAL
money = GAUGE_INITIAL
time = GAUGE_INITIAL
score = 0
game_over = False
game_over_message = ""

# --- Card Management ---
deck = list(CARDS)
random.shuffle(deck)
current_card = deck.pop()

# --- Helper Functions ---

def draw_text(text, font, color, surface, x, y, center=False):
    """General purpose function to draw text."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def wrap_text(text, font, max_width):
    """Wraps text to fit within a maximum width."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

def draw_gauges():
    """Draws the three resource gauges at the top of the screen."""
    gauge_width = 200
    gauge_height = 20
    
    # Energy Gauge
    draw_text("Energy", font_gauge, COLOR_WHITE, screen, 50, 20)
    pygame.draw.rect(screen, COLOR_DARK_GREY, (50, 45, gauge_width, gauge_height))
    pygame.draw.rect(screen, COLOR_ENERGY, (50, 45, energy * (gauge_width / GAUGE_MAX), gauge_height))

    # Money Gauge
    draw_text("Money", font_gauge, COLOR_WHITE, screen, 300, 20)
    pygame.draw.rect(screen, COLOR_DARK_GREY, (300, 45, gauge_width, gauge_height))
    pygame.draw.rect(screen, COLOR_MONEY, (300, 45, money * (gauge_width / GAUGE_MAX), gauge_height))

    # Time Gauge
    draw_text("Time", font_gauge, COLOR_WHITE, screen, 550, 20)
    pygame.draw.rect(screen, COLOR_DARK_GREY, (550, 45, gauge_width, gauge_height))
    pygame.draw.rect(screen, COLOR_TIME, (550, 45, time * (gauge_width / GAUGE_MAX), gauge_height))
    
    # Score
    draw_text(f"Score: {score}", font_gauge, COLOR_WHITE, screen, 350, 80)


def draw_card():
    """Draws the main card in the center of the screen."""
    card_rect = pygame.Rect(0, 0, 400, 300)
    card_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pygame.draw.rect(screen, COLOR_WHITE, card_rect, border_radius=15)
    
    # Draw wrapped text on the card
    wrapped_text = wrap_text(current_card["text"], font_card, card_rect.width - 40)
    for i, line in enumerate(wrapped_text):
        draw_text(line.strip(), font_card, COLOR_BLACK, screen, card_rect.centerx, card_rect.y + 40 + i * 35, center=True)
        
    # Draw instructions
    draw_text("◀ Deny", font_card, COLOR_DARK_GREY, screen, card_rect.left, card_rect.bottom + 20)
    draw_text("Agree ▶", font_card, COLOR_DARK_GREY, screen, card_rect.right, card_rect.bottom + 20, center=True)


def apply_effects(effects):
    """Applies the effects of a choice to the gauges and clamps values."""
    global energy, money, time, score
    
    energy += effects.get("energy", 0)
    money += effects.get("money", 0)
    time += effects.get("time", 0)

    # Clamp values between MIN and MAX
    energy = max(GAUGE_MIN, min(GAUGE_MAX, energy))
    money = max(GAUGE_MIN, min(GAUGE_MAX, money))
    time = max(GAUGE_MIN, min(GAUGE_MAX, time))
    
    score += 1

def check_game_over():
    """Checks if any gauge has reached a critical level."""
    global game_over, game_over_message
    if energy <= GAUGE_MIN:
        game_over = True
        game_over_message = "You ran out of energy!"
    elif energy >= GAUGE_MAX:
        game_over = True
        game_over_message = "You became supercharged and exploded!"
    elif money <= GAUGE_MIN:
        game_over = True
        game_over_message = "You went bankrupt!"
    elif money >= GAUGE_MAX:
        game_over = True
        game_over_message = "Your greed consumed you!"
    elif time <= GAUGE_MIN:
        game_over = True
        game_over_message = "You ran out of time!"
    elif time >= GAUGE_MAX:
        game_over = True
        game_over_message = "You got lost in the flow of time!"

def get_next_card():
    """Gets the next card from the deck, reshuffling if necessary."""
    global current_card, deck
    if not deck:
        deck = list(CARDS)
        random.shuffle(deck)
    current_card = deck.pop()


# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    apply_effects(current_card["left_effects"])
                    get_next_card()
                    check_game_over()
                elif event.key == pygame.K_RIGHT:
                    apply_effects(current_card["right_effects"])
                    get_next_card()
                    check_game_over()
            # Press any key to exit after game over
            elif game_over:
                running = False


    # --- Drawing ---
    screen.fill(COLOR_DARK_GREY)

    if not game_over:
        draw_gauges()
        draw_card()
    else:
        # Game Over Screen
        draw_text("GAME OVER", font_gameover, COLOR_WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, center=True)
        draw_text(game_over_message, font_card, COLOR_WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, center=True)
        draw_text(f"Final Score: {score}", font_card, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, center=True)
        draw_text("Press any key to exit.", font_gauge, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, center=True)


    # --- Update Display ---
    pygame.display.flip()
    clock.tick(60) # Limit frame rate to 60 FPS

# --- Quit ---
pygame.quit()
sys.exit()