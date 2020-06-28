import random
from pygame.locals import *

# GRID AND WINDOW SIZING #
TILE_WIDTH_PIXELS = 15
ROWS_IN_GRID = 36
COLUMNS_IN_GRID = 36
GRID_DIMENSIONS = (COLUMNS_IN_GRID * TILE_WIDTH_PIXELS, ROWS_IN_GRID * TILE_WIDTH_PIXELS)
BANNER_DIMENSIONS = (GRID_DIMENSIONS[0], 100)
DEFAULT_WINDOW_DIMENSIONS = (GRID_DIMENSIONS[0], GRID_DIMENSIONS[1] + BANNER_DIMENSIONS[1])
PIXELS_TRAVERSED_PER_UPDATE = TILE_WIDTH_PIXELS / 3

# SCORE #
POINTS_PER_LEVEL = 10

# COLORS #
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 30, 0)
LIGHT_GRAY = (220, 220, 220)
MEDIUM_GRAY = (246, 253, 255)
DARK_GRAY = (32, 32, 32)

GOLDEN = (255, 223, 0)
POISON = (100, 20, 110)
                # light color, medium color, dark color
GREY_PALETTE = ((255, 255, 255), (150, 150, 150), (0, 0, 0))
GREEN_PALETTE = ((120, 166, 108), (0, 130, 0), (0, 90, 50))
BLUE_PALETTE = ((97, 151, 213), (24, 97, 202), (11, 58, 125))
BROWN_PALETTE = ((125, 112, 96), (107, 68, 49), (74, 47, 21))
PURPLE_PALETTE = ((195, 165, 230), (130, 90, 195), (85, 25, 165))
RED_PALETTE = ((221, 176, 178), (173, 68, 73), (115, 13, 17))

def BLUE_SPECTRUM():
    r = 0
    g = random.randrange(65, 200)
    b = random.randrange(220, 245)
    return (r, g, b)

def GREEN_SPECTRUM():
    r = random.randrange(0, 15)
    g = random.randrange(95, 210)
    b = random.randrange(0, 35)
    return (r, g, b)

def PURPLE_SPECTRUM():
    r = random.randrange(80, 210)
    g = random.randrange(0, 50)
    b = random.randrange(200, 240)
    return (r, g, b)

def YARN_COLOR():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return (r, g, b)

# FONTS #
FONT_PATH = "fonts/"
STANDARD_FONT = "rajdhani.ttf"
FONT_SIZE_XSMALL = int(TILE_WIDTH_PIXELS * 1.6)
FONT_SIZE_SMALL = int(TILE_WIDTH_PIXELS * 1.8)
FONT_SIZE_MEDIUM = int(TILE_WIDTH_PIXELS * 2.4)
FONT_SIZE_LARGE = int(TILE_WIDTH_PIXELS * 3)
FONT_SIZE_HUGE = int(TILE_WIDTH_PIXELS * 5.5)
FONT_SIZE_GIANT = int(TILE_WIDTH_PIXELS * 8)

# Keys #
ARROW_KEYS = [K_a, K_w, K_d, K_s, K_LEFT, K_UP, K_RIGHT, K_DOWN]

# SOUNDS #
SOUND_PATH = "sounds/"
BEEP1_SOUND = "beep1.wav"
BEEP2_SOUND = "beep2.wav"
GLOSS_SOUND = "gloss.wav"
CHIME_LOW_SOUND = "chimelow.wav"
CHIME_HIGH_SOUND = "chimehigh.wav"
DING_SOUND = "ding.wav"
VICTORY_SOUND = "victory.wav"
LOSS_SOUND = "loss.wav"
LEVEL_ANNOUNCEMENT_SOUNDS = (
    "level_one.wav",
    "level_two.wav",
    "level_three.wav",
    "level_four.wav",
    "level_five.wav",
    "level_six.wav",
    "level_seven.wav",
    "level_eight.wav",
    "level_nine.wav",
    "level_last.wav",
)
# Sound effects obtained from zapsplat.com
# TTS files obtained from ibm.com/cloud/watson-text-to-speech

