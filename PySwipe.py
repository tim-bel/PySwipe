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
CARD_WIDTH = 400
CARD_HEIGHT = 450

# Colors
COLOR_BACKGROUND = (40, 40, 50)
COLOR_WHITE = (255, 255, 255)
COLOR_CARD_BG = (245, 245, 245)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (200, 200, 200)
COLOR_DARK_GREY = (50, 50, 50)
COLOR_INSTRUCTION = (150, 150, 150)
COLOR_ENERGY = (80, 220, 80)      # Brighter Green
COLOR_MONEY = (255, 220, 80)      # Brighter Gold
COLOR_TIME = (100, 180, 255)    # Lighter Blue
COLOR_PREVIEW_NEG = (200, 50, 50) # Red for negative preview

# Game Parameters
GAUGE_MIN = 0
GAUGE_MAX = 100
GAUGE_INITIAL = 50

# --- Card Deck ---
# Each card has a text description, effects, and an image.
CARDS = [
    # Existing Cards
    {
        "text": "A dragon is attacking a nearby village! Intervene?",
        "right_effects": {"energy": -30, "money": 50, "time": -25},
        "left_effects": {"energy": -5, "money": -10, "time": -5},
        "image": "images/dragon.png"
    },
    {
        "text": "A shady merchant offers a 'shortcut' through the haunted forest.",
        "right_effects": {"energy": -10, "money": -15, "time": 25},
        "left_effects": {"energy": 0, "money": 0, "time": -15},
        "image": "images/merchant.png"
    },
    {
        "text": "The King requests an audience. He seems bored. Entertain him?",
        "right_effects": {"energy": -15, "money": 20, "time": -20},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/king.png"
    },
    {
        "text": "You find a mysterious, glowing mushroom. Eat it?",
        "right_effects": {"energy": 40, "money": -5, "time": -5},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/mushroom.png"
    },
    {
        "text": "A traveling circus is in town. Spend the day watching shows?",
        "right_effects": {"energy": 20, "money": -20, "time": -25},
        "left_effects": {"energy": 5, "money": 0, "time": -5},
        "image": "images/circus.png"
    },
    {
        "text": "Your rival challenges you to a duel at dawn.",
        "right_effects": {"energy": -25, "money": 25, "time": -10},
        "left_effects": {"energy": -10, "money": -10, "time": -5},
        "image": "images/duel.png"
    },
    {
        "text": "A powerful wizard offers to enchant your gear for a hefty price.",
        "right_effects": {"energy": 10, "money": -40, "time": -15},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/wizard.png"
    },
    {
        "text": "Spend all night at the tavern gambling and drinking?",
        "right_effects": {"energy": -20, "money": 35, "time": -20},
        "left_effects": {"energy": 10, "money": 0, "time": -5},
        "image": "images/tavern.png"
    },
    # New Cards
    {
        "text": "Invest in a new trading route to the East.",
        "right_effects": {"energy": -10, "money": 50, "time": -30},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/trade_route.png"
    },
    {
        "text": "A famine strikes the northern provinces. Send aid?",
        "right_effects": {"energy": -10, "money": -30, "time": -15},
        "left_effects": {"energy": 0, "money": 0, "time": 0},
        "image": "images/famine.png"
    },
    {
        "text": "The royal alchemist needs a rare herb from the mountains.",
        "right_effects": {"energy": -20, "money": 25, "time": -20},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/alchemist.png"
    },
    {
        "text": "A group of bards wants to write a song about your adventures.",
        "right_effects": {"energy": 5, "money": 10, "time": -15},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/bards.png"
    },
    {
        "text": "You discover an ancient library hidden beneath the city.",
        "right_effects": {"energy": -5, "money": 0, "time": 30},
        "left_effects": {"energy": 0, "money": 0, "time": -10},
        "image": "images/library.png"
    },
    {
        "text": "A plague is spreading in the slums. Quarantine the area?",
        "right_effects": {"energy": -15, "money": -20, "time": -25},
        "left_effects": {"energy": 0, "money": -10, "time": -10},
        "image": "images/plague.png"
    },
    {
        "text": "A foreign diplomat arrives with a proposal of alliance.",
        "right_effects": {"energy": -5, "money": 20, "time": -20},
        "left_effects": {"energy": 0, "money": -15, "time": -5},
        "image": "images/diplomat.png"
    },
    {
        "text": "A group of miners has gone on strike. Negotiate with them?",
        "right_effects": {"energy": -10, "money": -10, "time": -15},
        "left_effects": {"energy": 0, "money": -25, "time": -10},
        "image": "images/miners.png"
    },
    {
        "text": "A new philosophy is gaining popularity. Suppress it?",
        "right_effects": {"energy": -5, "money": -10, "time": -15},
        "left_effects": {"energy": 0, "money": 5, "time": -5},
        "image": "images/philosophy.png"
    },
    {
        "text": "A master thief offers to teach you their skills.",
        "right_effects": {"energy": -15, "money": 25, "time": -20},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/thief.png"
    },
    {
        "text": "You have a chance to sabotage your rival's business.",
        "right_effects": {"energy": -10, "money": 30, "time": -15},
        "left_effects": {"energy": 0, "money": -10, "time": -5},
        "image": "images/sabotage.png"
    },
    {
        "text": "A powerful artifact is discovered. Claim it for the kingdom?",
        "right_effects": {"energy": -20, "money": 40, "time": -25},
        "left_effects": {"energy": 0, "money": -10, "time": -5},
        "image": "images/artifact.png"
    },
    {
        "text": "The city guard is demanding higher wages.",
        "right_effects": {"energy": -5, "money": -25, "time": -10},
        "left_effects": {"energy": 0, "money": -15, "time": -10},
        "image": "images/guard.png"
    },
    {
        "text": "A traveling artist offers to paint your portrait.",
        "right_effects": {"energy": 5, "money": -10, "time": -15},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/artist.png"
    },
    {
        "text": "A noble is plotting against the King. Expose them?",
        "right_effects": {"energy": -10, "money": 30, "time": -20},
        "left_effects": {"energy": 0, "money": -15, "time": -5},
        "image": "images/plot.png"
    },
    {
        "text": "A new technology is invented. Fund its development?",
        "right_effects": {"energy": -10, "money": -30, "time": 25},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/technology.png"
    },
    {
        "text": "A group of peasants is protesting high taxes.",
        "right_effects": {"energy": -10, "money": -15, "time": -15},
        "left_effects": {"energy": 0, "money": -20, "time": -10},
        "image": "images/protest.png"
    },
    {
        "text": "A mysterious stranger gives you a locked box.",
        "right_effects": {"energy": -5, "money": 15, "time": -10},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/box.png"
    },
    {
        "text": "A famous explorer asks for funding for an expedition.",
        "right_effects": {"energy": -10, "money": -25, "time": 30},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/explorer.png"
    },
    {
        "text": "A ghost is haunting the royal palace. Investigate?",
        "right_effects": {"energy": -15, "money": 10, "time": -20},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/ghost.png"
    },
    {
        "text": "A rare comet is passing. Host a festival to celebrate?",
        "right_effects": {"energy": 15, "money": -20, "time": -20},
        "left_effects": {"energy": 5, "money": 0, "time": -5},
        "image": "images/comet.png"
    },
    {
        "text": "A magical spring is discovered. Commercialize it?",
        "right_effects": {"energy": 10, "money": 30, "time": -15},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/spring.png"
    },
    {
        "text": "A group of scholars wants to establish a university.",
        "right_effects": {"energy": -5, "money": -20, "time": 25},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/university.png"
    },
    {
        "text": "A secret society invites you to join their ranks.",
        "right_effects": {"energy": -10, "money": 20, "time": -20},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/society.png"
    },
    {
        "text": "A prophecy foretells your doom. Consult an oracle?",
        "right_effects": {"energy": -5, "money": -10, "time": -15},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/prophecy.png"
    },
    {
        "text": "Your childhood friend is in trouble. Help them?",
        "right_effects": {"energy": -15, "money": -10, "time": -20},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/friend.png"
    },
    {
        "text": "A valuable shipwreck is discovered off the coast.",
        "right_effects": {"energy": -20, "money": 40, "time": -25},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/shipwreck.png"
    },
    {
        "text": "A tribe of nomads offers to trade rare goods.",
        "right_effects": {"energy": -5, "money": 20, "time": -15},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/nomads.png"
    },
    {
        "text": "A beast is terrorizing the countryside. Hunt it down?",
        "right_effects": {"energy": -25, "money": 30, "time": -20},
        "left_effects": {"energy": 0, "money": -10, "time": -5},
        "image": "images/beast.png"
    },
    {
        "text": "A great storm is approaching. Prepare the city?",
        "right_effects": {"energy": -15, "money": -20, "time": -20},
        "left_effects": {"energy": 0, "money": -10, "time": -10},
        "image": "images/storm.png"
    },
    {
        "text": "A charismatic leader is rallying the common folk.",
        "right_effects": {"energy": -10, "money": -10, "time": -15},
        "left_effects": {"energy": 0, "money": 5, "time": -5},
        "image": "images/leader.png"
    },
    {
        "text": "A cursed treasure is unearthed. Destroy it?",
        "right_effects": {"energy": -10, "money": 10, "time": -15},
        "left_effects": {"energy": 0, "money": -5, "time": -5},
        "image": "images/treasure.png"
    },
    {
        "text": "The kingdom's spies have been compromised.",
        "right_effects": {"energy": -15, "money": -20, "time": -25},
        "left_effects": {"energy": 0, "money": -10, "time": -10},
        "image": "images/spies.png"
    },
    {
        "text": "A rare celestial event is happening. Study it?",
        "right_effects": {"energy": -5, "money": -5, "time": 20},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/celestial.png"
    },
    {
        "text": "A gladiator tournament is being held. Participate?",
        "right_effects": {"energy": -20, "money": 30, "time": -20},
        "left_effects": {"energy": 5, "money": -5, "time": -5},
        "image": "images/gladiator.png"
    },
    {
        "text": "A new continent has been discovered. Launch an expedition?",
        "right_effects": {"energy": -25, "money": -40, "time": 40},
        "left_effects": {"energy": 0, "money": -10, "time": -5},
        "image": "images/continent.png"
    },
    {
        "text": "A hermit living in the woods claims to know the future.",
        "right_effects": {"energy": -5, "money": -10, "time": -10},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/hermit.png"
    },
    {
        "text": "The royal treasury is running low. Raise taxes?",
        "right_effects": {"energy": -10, "money": 30, "time": -15},
        "left_effects": {"energy": 0, "money": -20, "time": -10},
        "image": "images/taxes.png"
    },
    {
        "text": "A legendary blacksmith can forge a powerful weapon for you.",
        "right_effects": {"energy": -10, "money": -35, "time": -20},
        "left_effects": {"energy": 0, "money": 0, "time": -5},
        "image": "images/blacksmith.png"
    },
    {
        "text": "A trade guild is trying to monopolize the market.",
        "right_effects": {"energy": -10, "money": -20, "time": -15},
        "left_effects": {"energy": 0, "money": 25, "time": -10},
        "image": "images/guild.png"
    },
    {
        "text": "A rebellion is brewing in a distant province.",
        "right_effects": {"energy": -25, "money": -30, "time": -30},
        "left_effects": {"energy": 0, "money": -15, "time": -10},
        "image": "images/rebellion.png"
    }
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
highscore = 0
game_over = False
game_over_message = ""

# Animation & Image State
card_pos_x = SCREEN_WIDTH + CARD_WIDTH
card_target_x = SCREEN_WIDTH / 2
card_animation_speed = 20  # Smaller is faster
swiping = None # Can be 'left', 'right', or None
card_images = {} # Cache for loaded card images


# --- Card Management ---
deck = list(CARDS)
random.shuffle(deck)
current_card = None # Will be set by get_next_card


def load_highscore():
    """Loads the highscore from the file."""
    global highscore
    try:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())
    except (IOError, ValueError):
        highscore = 0

def save_highscore():
    """Saves the highscore to the file."""
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))

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

def draw_gauges(preview_effects=None):
    """Draws the three resource gauges, optionally with a preview of changes."""
    gauge_width = 200
    gauge_height = 20

    def draw_single_gauge(name, value, color, x, y, effect_key):
        draw_text(name, font_gauge, COLOR_WHITE, screen, x, y)
        # Base gauge
        pygame.draw.rect(screen, COLOR_DARK_GREY, (x, y + 25, gauge_width, gauge_height))
        pygame.draw.rect(screen, color, (x, y + 25, value * (gauge_width / GAUGE_MAX), gauge_height))

        # Preview effect
        if preview_effects:
            change = preview_effects.get(effect_key, 0)
            if change != 0:
                preview_value = max(GAUGE_MIN, min(GAUGE_MAX, value + change))
                current_width = value * (gauge_width / GAUGE_MAX)
                preview_width = preview_value * (gauge_width / GAUGE_MAX)

                if change > 0:  # Increase
                    preview_rect = pygame.Rect(x + current_width, y + 25, preview_width - current_width, gauge_height)
                    pygame.draw.rect(screen, tuple(min(255, c + 80) for c in color), preview_rect)
                else:  # Decrease
                    preview_rect = pygame.Rect(x + preview_width, y + 25, current_width - preview_width, gauge_height)
                    pygame.draw.rect(screen, COLOR_PREVIEW_NEG, preview_rect)

    draw_single_gauge("Energy", energy, COLOR_ENERGY, 50, 20, "energy")
    draw_single_gauge("Money", money, COLOR_MONEY, 300, 20, "money")
    draw_single_gauge("Time", time, COLOR_TIME, 550, 20, "time")

    # Score and Highscore
    draw_text(f"Score: {score}", font_gauge, COLOR_WHITE, screen, SCREEN_WIDTH / 2, 80, center=True)
    draw_text(f"High Score: {highscore}", font_gauge, COLOR_WHITE, screen, SCREEN_WIDTH / 2, 110, center=True)


def draw_card():
    """Draws the main card, including its image and text, at its current animated position."""
    if not current_card:
        return

    card_rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
    card_rect.center = (card_pos_x, SCREEN_HEIGHT / 2 + 30)

    pygame.draw.rect(screen, COLOR_CARD_BG, card_rect, border_radius=15)

    # Draw Card Image
    image_path = current_card.get("image")
    if image_path:
        if image_path not in card_images:
            try:
                card_images[image_path] = pygame.image.load(image_path).convert_alpha()
            except (pygame.error, FileNotFoundError):
                card_images[image_path] = None # Mark as failed to load

        loaded_image = card_images[image_path]
        if loaded_image:
            img_rect = loaded_image.get_rect()

            # Maintain aspect ratio
            scale = min((CARD_WIDTH - 40) / img_rect.width, 180 / img_rect.height)
            scaled_size = (int(img_rect.width * scale), int(img_rect.height * scale))
            scaled_image = pygame.transform.smoothscale(loaded_image, scaled_size)

            img_x = card_rect.centerx - scaled_image.get_width() / 2
            img_y = card_rect.top + 20
            screen.blit(scaled_image, (img_x, img_y))

    # Draw wrapped text on the card, below the image
    text_y_start = card_rect.top + 230
    wrapped_text = wrap_text(current_card["text"], font_card, card_rect.width - 40)
    for i, line in enumerate(wrapped_text):
        draw_text(line.strip(), font_card, COLOR_BLACK, screen, card_rect.centerx, text_y_start + i * 35, center=True)

    # Draw instructions
    draw_text("◀ Deny", font_card, COLOR_INSTRUCTION, screen, card_rect.left, card_rect.bottom + 20)
    draw_text("Agree ▶", font_card, COLOR_INSTRUCTION, screen, card_rect.right - font_card.size("Agree ▶")[0], card_rect.bottom + 20)


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
    global game_over, game_over_message, highscore

    is_over = False
    if energy <= GAUGE_MIN:
        is_over = True
        game_over_message = "You ran out of energy!"
    elif energy >= GAUGE_MAX:
        is_over = True
        game_over_message = "You became supercharged and exploded!"
    elif money <= GAUGE_MIN:
        is_over = True
        game_over_message = "You went bankrupt!"
    elif money >= GAUGE_MAX:
        is_over = True
        game_over_message = "Your greed consumed you!"
    elif time <= GAUGE_MIN:
        is_over = True
        game_over_message = "You ran out of time!"
    elif time >= GAUGE_MAX:
        is_over = True
        game_over_message = "You got lost in the flow of time!"

    if is_over:
        game_over = True
        if score > highscore:
            highscore = score
            save_highscore()

def get_next_card():
    """Gets the next card from the deck, reshuffling if necessary, and resets its animation state."""
    global current_card, deck, card_pos_x, card_target_x
    if not deck:
        deck = list(CARDS)
        random.shuffle(deck)

    current_card = deck.pop()
    card_pos_x = SCREEN_WIDTH + CARD_WIDTH / 2
    card_target_x = SCREEN_WIDTH / 2


# --- Main Game Loop ---
load_highscore()
get_next_card()
running = True
while running:
    # --- Animation ---
    if not game_over:
        dx = card_target_x - card_pos_x
        if abs(dx) < 1:
            card_pos_x = card_target_x
            if swiping:
                effects = current_card[f"{swiping}_effects"]
                apply_effects(effects)
                check_game_over()
                if not game_over:
                    get_next_card()
                swiping = None
        else:
            card_pos_x += dx / card_animation_speed

    # --- Event Handling ---
    mouse_pos = pygame.mouse.get_pos()
    preview_effects = None
    if not game_over and current_card:
        if mouse_pos[0] < SCREEN_WIDTH / 2:
            preview_effects = current_card["left_effects"]
        else:
            preview_effects = current_card["right_effects"]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over and not swiping and current_card:
                if event.key == pygame.K_LEFT:
                    swiping = 'left'
                    card_target_x = -CARD_WIDTH / 2
                elif event.key == pygame.K_RIGHT:
                    swiping = 'right'
                    card_target_x = SCREEN_WIDTH + CARD_WIDTH / 2
            elif game_over:
                running = False


    # --- Drawing ---
    screen.fill(COLOR_BACKGROUND)

    if not game_over:
        draw_gauges(preview_effects)
        draw_card()
    else:
        # Game Over Screen
        draw_text("GAME OVER", font_gameover, COLOR_WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, center=True)
        draw_text(game_over_message, font_card, COLOR_WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, center=True)
        draw_text(f"Final Score: {score}", font_card, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, center=True)
        draw_text(f"High Score: {highscore}", font_card, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80, center=True)
        draw_text("Press any key to exit.", font_gauge, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120, center=True)


    # --- Update Display ---
    pygame.display.flip()
    clock.tick(60)

# --- Quit ---
pygame.quit()
sys.exit()