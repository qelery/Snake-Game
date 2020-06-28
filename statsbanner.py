import pygame
from config import *


class StatsBanner:
    """
    The stats banner at the top of the window.

    Displays the player's score and the level.

    ...

    Attributes
    ----------
    dimensions: tuple of int
        dimensions of the banner in pixels
    color : tuple of int
        the rgb value of the banner's background
    background : pygame.Surface
        a rectangular graphic representing the banner
    rect : pygame.Rect
        coordinates of the banner
    score_text : pygame.Surface
        a rectangular graphic showing the current score
    score_rect : pygame.Rect
        coordinates of the score text
    level_text : pygame.Surface
        a rectangular graphic showing the current level
    level_rect : pygame.Rect
        coordinates of the level text

    Methods
    -------
    change_color(color)
        change the color of the banner's background
    announce_level_change()
        play an audio file announcing the current level
    update()
        update the score and level text
    draw()
        draw the banner to the screen
    """
    def __init__(self, grid_dimensions, color):
        self.dimensions = grid_dimensions[0], 100
        self.color = color
        self.background = pygame.Surface(self.dimensions).convert()
        self.background.fill(color)
        self.rect = self.background.get_rect()
        self.rect.topleft = 0, 0
        self.font = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_SMALL)
        self.score_text = None
        self.level_text = None
        self.score_rect = None
        self.level_rect = None
        self.score = 0
        self.level = 1

    def change_color(self, color):
        self.color = color
        self.background.fill(self.color)

    def announce_level_change(self):
        pygame.mixer.Sound(SOUND_PATH + GLOSS_SOUND)
        pygame.mixer.Sound(SOUND_PATH + LEVEL_ANNOUNCEMENT_SOUNDS[self.level-1]).play()

    def update(self):
        score_text = f"SCORE:   {self.score:02d}"
        level_text = f"LEVEL:   {self.level:02d}"
        self.score_text = self.font.render(score_text, True, WHITE, self.color)
        self.level_text = self.font.render(level_text, True, WHITE, self.color)
        self.score_rect = self.score_text.get_rect()
        self.level_rect = self.level_text.get_rect()
        self.score_rect.center = (self.dimensions[0] * 0.25, self.dimensions[1] * 0.5)
        self.level_rect.center = (self.dimensions[0] * 0.75, self.dimensions[1] * 0.5)

    def draw(self, surface):
        surface.blit(self.background, self.rect)
        surface.blit(self.score_text, self.score_rect)
        surface.blit(self.level_text, self.level_rect)

