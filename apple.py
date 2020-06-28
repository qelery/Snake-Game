import pygame
from config import *


class Apple:
    """"
    Creates a colored square that represents an apple.

    A point is scored when the snake collides with an apple
    Red colored apples slightly grow the snake.
    Poison colored apples rapidly grow the snake.
    Golden colored apples shrink the snake.

    ...

    Attributes
    ----------
    image : pygame.Surface
        a graphic representing the apple
    rect : pygame.Rect
        coordinates of apple
    color : tuple of int
        rgb color of the apple
    eaten_sound: Sound
        the sound that is played whenever the snake collides with the apple

    Methods
    -------
    move_to(x, y)
        Move the apple to the specified location on the grid
    draw(surface)
        Draw the apple to the screen
    """
    def __init__(self, color):
        self.image = pygame.Surface((TILE_WIDTH_PIXELS, TILE_WIDTH_PIXELS)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.color = color
        self.eaten_sound = self._assign_sound()

    def _assign_sound(self):
        if self.color == RED:
            return pygame.mixer.Sound(SOUND_PATH + BEEP1_SOUND)
        elif self.color == POISON:
            return pygame.mixer.Sound(SOUND_PATH + BEEP2_SOUND)
        elif self.color == GOLDEN:
            return pygame.mixer.Sound(SOUND_PATH + GLOSS_SOUND)

    def move_to(self, x, y):
        self.rect.topleft = x, y

    def draw(self, surface):
        surface.blit(self.image, self.rect)