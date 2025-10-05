import pygame
import random
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
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
COLOR_SANITY = (200, 120, 255)   # Light Purple for Sanity
COLOR_PREVIEW_NEG = (200, 50, 50) # Red for negative preview

# Game Parameters
GAUGE_MIN = 0
GAUGE_MAX = 100
GAUGE_INITIAL = 50

# --- Card Deck (Modern Life Theme) ---
# Cards are rebalanced for longer gameplay with smaller increments.
CARDS = [
    # --- Work Themed Cards ---
    {
        "text": "Your boss asks you to work over the weekend for a 'critical' deadline.",
        "right_effects": {"energy": -20, "money": 25, "sanity": -15},
        "left_effects": {"energy": 5, "money": 0, "sanity": 5},
        "image": "images/work_weekend.png"
    },
    {
        "text": "A recruiter reaches out on LinkedIn with a 'once in a lifetime' opportunity.",
        "right_effects": {"energy": -10, "money": 0, "sanity": -10},
        "left_effects": {"energy": 0, "money": 0, "sanity": 0},
        "image": "images/recruiter.png"
    },
    {
        "text": "It's 2 PM. Do you power through the slump or take a 20-minute coffee break?",
        "right_effects": {"energy": 10, "money": -5, "sanity": 5},
        "left_effects": {"energy": -10, "money": 0, "sanity": -5},
        "image": "images/coffee.png"
    },
    {
        "text": "Team lunch at that expensive place everyone loves. Do you join?",
        "right_effects": {"energy": 5, "money": -20, "sanity": 10},
        "left_effects": {"energy": 0, "money": 0, "sanity": -5},
        "image": "images/team_lunch.png"
    },
    {
        "text": "You're asked to take on a 'stretch project' that's well outside your job description.",
        "right_effects": {"energy": -15, "money": 0, "sanity": -20},
        "left_effects": {"energy": 0, "money": 0, "sanity": 5},
        "image": "images/stretch_project.png"
    },
    {
        "text": "An email from your boss arrives at 9 PM. Do you open it?",
        "right_effects": {"energy": -5, "money": 0, "sanity": -15},
        "left_effects": {"energy": 0, "money": 0, "sanity": 10},
        "image": "images/late_email.png"
    },
    # --- Finance Themed Cards ---
    {
        "text": "Your favorite streaming service just hiked its price again. Keep subscription?",
        "right_effects": {"energy": 0, "money": -10, "sanity": 5},
        "left_effects": {"energy": 0, "money": 0, "sanity": -5},
        "image": "images/streaming.png"
    },
    {
        "text": "Groceries cost a fortune. Splurge on organic produce or buy instant noodles?",
        "right_effects": {"energy": 10, "money": -15, "sanity": 5},
        "left_effects": {"energy": -10, "money": 5, "sanity": -5},
        "image": "images/groceries.png"
    },
    {
        "text": "Your friend is hyping up a new cryptocurrency. Invest your savings?",
        "right_effects": {"energy": -5, "money": 0, "sanity": -20}, # Represents risk, not actual loss/gain
        "left_effects": {"energy": 0, "money": 0, "sanity": 0},
        "image": "images/crypto.png"
    },
    {
        "text": "The 'Check Engine' light on your car just came on. Deal with it now?",
        "right_effects": {"energy": -5, "money": -25, "sanity": 10},
        "left_effects": {"energy": 0, "money": 0, "sanity": -10},
        "image": "images/car_trouble.png"
    },
    {
        "text": "You get an unexpected small bonus. Put it into savings?",
        "right_effects": {"energy": 0, "money": 20, "sanity": 15},
        "left_effects": {"energy": 10, "money": 0, "sanity": -5},
        "image": "images/bonus.png"
    },
    {
        "text": "Student loan payments are due. Pay the minimum or an extra chunk?",
        "right_effects": {"energy": 0, "money": -25, "sanity": 10},
        "left_effects": {"energy": 0, "money": -15, "sanity": -5},
        "image": "images/student_loan.png"
    },
     # --- Health & Wellness Cards ---
    {
        "text": "It's dark and cold, but you know you should go to the gym. Go?",
        "right_effects": {"energy": 20, "money": -5, "sanity": 10},
        "left_effects": {"energy": -10, "money": 0, "sanity": -5},
        "image": "images/gym.png"
    },
    {
        "text": "You have a lingering cough. Take a sick day to rest?",
        "right_effects": {"energy": 25, "money": -15, "sanity": 10},
        "left_effects": {"energy": -15, "money": 0, "sanity": -10},
        "image": "images/sick_day.png"
    },
    {
        "text": "It's been a long day. Order greasy takeout for dinner?",
        "right_effects": {"energy": 10, "money": -15, "sanity": 5},
        "left_effects": {"energy": -5, "money": 0, "sanity": -10},
        "image": "images/takeout.png"
    },
    {
        "text": "Your phone says you've been doomscrolling for an hour. Put it down?",
        "right_effects": {"energy": 5, "money": 0, "sanity": 15},
        "left_effects": {"energy": -10, "money": 0, "sanity": -15},
        "image": "images/doomscroll.png"
    },
    {
        "text": "Your annual physical is overdue. Schedule an appointment?",
        "right_effects": {"energy": 0, "money": -20, "sanity": 10},
        "left_effects": {"energy": -5, "money": 0, "sanity": -10},
        "image": "images/doctor.png"
    },
    {
        "text": "Feeling completely burnt out. Meditate for 10 minutes?",
        "right_effects": {"energy": 5, "money": 0, "sanity": 20},
        "left_effects": {"energy": -5, "money": 0, "sanity": -5},
        "image": "images/meditate.png"
    },
    # --- Social & Lifestyle Cards ---
    {
        "text": "Friends want to go out for expensive cocktails. Do you go?",
        "right_effects": {"energy": -10, "money": -20, "sanity": 15},
        "left_effects": {"energy": 5, "money": 0, "sanity": -10},
        "image": "images/cocktails.png"
    },
    {
        "text": "Your parents call for the third time this week. Pick up?",
        "right_effects": {"energy": -10, "money": 0, "sanity": -5},
        "left_effects": {"energy": 0, "money": 0, "sanity": 5},
        "image": "images/phone_call.png"
    },
    {
        "text": "It's your friend's destination wedding. Can you really afford to go?",
        "right_effects": {"energy": -15, "money": -30, "sanity": 10},
        "left_effects": {"energy": 0, "money": 0, "sanity": -15},
        "image": "images/wedding.png"
    },
    {
        "text": "That pile of laundry isn't going to do itself. Tackle it now?",
        "right_effects": {"energy": -10, "money": 0, "sanity": 15},
        "left_effects": {"energy": 0, "money": 0, "sanity": -10},
        "image": "images/laundry.png"
    },
    {
        "text": "A new season of that show everyone's talking about just dropped. Binge it all?",
        "right_effects": {"energy": -15, "money": 0, "sanity": 10},
        "left_effects": {"energy": 5, "money": 0, "sanity": 0},
        "image": "images/binge_watch.png"
    },
    {
        "text": "Your pet looks bored. Spend 30 minutes playing with them?",
        "right_effects": {"energy": -5, "money": 0, "sanity": 20},
        "left_effects": {"energy": 0, "money": 0, "sanity": -5},
        "image": "images/pet.png"
    },
    {
        "text": "It's a beautiful day. Spend your lunch break outside?",
        "right_effects": {"energy": 15, "money": 0, "sanity": 10},
        "left_effects": {"energy": -5, "money": 0, "sanity": -5},
        "image": "images/outside.png"
    }
]

# Create a larger deck by duplicating the base cards to ensure enough for a 5-minute game
FULL_DECK = CARDS * 2

# --- Setup Screen and Fonts ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Modern Life Survival")
clock = pygame.time.Clock()

font_gauge = pygame.font.Font(None, FONT_SIZE_GAUGE)
font_card = pygame.font.Font(None, FONT_SIZE_CARD)
font_gameover = pygame.font.Font(None, FONT_SIZE_GAMEOVER)

# --- Game State Variables ---
energy = GAUGE_INITIAL
money = GAUGE_INITIAL
sanity = GAUGE_INITIAL
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
deck = list(FULL_DECK)
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
    draw_single_gauge("Sanity", sanity, COLOR_SANITY, 550, 20, "sanity")

    # Score and Highscore
    draw_text(f"Days Survived: {score}", font_gauge, COLOR_WHITE, screen, SCREEN_WIDTH / 2, 80, center=True)
    draw_text(f"Best Streak: {highscore}", font_gauge, COLOR_WHITE, screen, SCREEN_WIDTH / 2, 110, center=True)


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
    draw_text("◀ No", font_card, COLOR_INSTRUCTION, screen, card_rect.left, card_rect.bottom + 20)
    draw_text("Yes ▶", font_card, COLOR_INSTRUCTION, screen, card_rect.right - font_card.size("Yes ▶")[0], card_rect.bottom + 20)


def apply_effects(effects):
    """Applies the effects of a choice to the gauges and clamps values."""
    global energy, money, sanity, score

    energy += effects.get("energy", 0)
    money += effects.get("money", 0)
    sanity += effects.get("sanity", 0)

    # Clamp values between MIN and MAX
    energy = max(GAUGE_MIN, min(GAUGE_MAX, energy))
    money = max(GAUGE_MIN, min(GAUGE_MAX, money))
    sanity = max(GAUGE_MIN, min(GAUGE_MAX, sanity))

    score += 1

def check_game_over():
    """Checks if any gauge has reached a critical level."""
    global game_over, game_over_message, highscore

    is_over = False
    if energy <= GAUGE_MIN:
        is_over = True
        game_over_message = "You collapsed from exhaustion."
    elif energy >= GAUGE_MAX:
        is_over = True
        game_over_message = "You had so much energy you couldn't sleep for a week."
    elif money <= GAUGE_MIN:
        is_over = True
        game_over_message = "Your bank account is empty."
    elif money >= GAUGE_MAX:
        is_over = True
        game_over_message = "You became a victim of your own lifestyle inflation."
    elif sanity <= GAUGE_MIN:
        is_over = True
        game_over_message = "You're completely burnt out."
    elif sanity >= GAUGE_MAX:
        is_over = True
        game_over_message = "You achieved ultimate zen and left society."

    if is_over:
        game_over = True
        if score > highscore:
            highscore = score
            save_highscore()

def get_next_card():
    """Gets the next card from the deck, reshuffling if necessary, and resets its animation state."""
    global current_card, deck, card_pos_x, card_target_x
    if not deck:
        deck = list(FULL_DECK)
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
                # Restart game on key press
                energy = GAUGE_INITIAL
                money = GAUGE_INITIAL
                sanity = GAUGE_INITIAL
                score = 0
                game_over = False
                get_next_card()


    # --- Drawing ---
    screen.fill(COLOR_BACKGROUND)

    if not game_over:
        draw_gauges(preview_effects)
        draw_card()
    else:
        # Game Over Screen
        draw_text("GAME OVER", font_gameover, COLOR_WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, center=True)
        draw_text(game_over_message, font_card, COLOR_WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, center=True)
        draw_text(f"You Survived: {score} Days", font_card, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, center=True)
        draw_text(f"Best Streak: {highscore} Days", font_card, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80, center=True)
        draw_text("Press any key to try again.", font_gauge, COLOR_GREY, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120, center=True)


    # --- Update Display ---
    pygame.display.flip()
    clock.tick(60)

# --- Quit ---
pygame.quit()
sys.exit()
