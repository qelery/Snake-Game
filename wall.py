import pygame
from config import *


class BrickWall():
    """
    A wall of bricks that surrounds the perimeter of the playing grid.

    There's a small gap in each wall for the snake to pass through.
    The game is over if the snake touches any part of the wall.

    ...

    Attributes
    ----------
    grid_dimensions : tuple of int
        dimensions of the game's playing grid
    color : tuple
        rgb color value
    bricks : list of Brick
        all of the bricks that make up the wall

    Methods
    ------
    change_color(color)
        change the color of all bricks in the wall
    draw(surface)
        Draw the wall to the screen
    """
    def __init__(self, grid_dimensions, color):
        self.grid_dimensions = grid_dimensions
        self.color = color
        self.bricks = []
        self._place_bricks()

    def _place_bricks(self):
        """Places the bricks that will make up the wall along the perimeter of the playing grid."""
        bricks_per_horizontal_wall = int((self.grid_dimensions[0] / TILE_WIDTH_PIXELS) * 0.5)
        bricks_per_vertical_wall = int((self.grid_dimensions[1] / TILE_WIDTH_PIXELS) * 0.5)

        # build top and right walls
        x_position = 0
        y_position = BANNER_DIMENSIONS[1]
        top_wall = [Brick(self.color) for _ in range(bricks_per_horizontal_wall)]
        right_wall = [Brick(self.color) for _ in range(bricks_per_vertical_wall)]
        for brick in top_wall:
            brick.rect.move_ip(x_position, y_position)
            x_position += TILE_WIDTH_PIXELS * 2
        x_position -= TILE_WIDTH_PIXELS * 2
        for brick in right_wall:
            brick.rect.move_ip(x_position, y_position)
            y_position += TILE_WIDTH_PIXELS * 2

        # if even number of bricks in wall, create gap size that is odd number to keep wall symmetrical
        # vice-versa for odd number of bricks in wall
        if bricks_per_horizontal_wall % 2 == 0:
            horizontal_gap_len = 8
        else:
            horizontal_gap_len = 7
        if bricks_per_vertical_wall % 2 == 0:
            vertical_gap_len = 8
        else:
            vertical_gap_len = 7
        t = int((bricks_per_horizontal_wall - horizontal_gap_len) / 2)
        top_wall = top_wall[:t] + top_wall[t + horizontal_gap_len:]
        r = int((bricks_per_vertical_wall - vertical_gap_len) / 2)
        right_wall = right_wall[:r] + right_wall[r + vertical_gap_len:]

        # mirror top and right walls
        # copy.deepcopy doesn't work on rect objects
        left_wall = [Brick(self.color) for _ in range(bricks_per_vertical_wall)]
        bottom_wall = [Brick(self.color) for _ in range(bricks_per_horizontal_wall)]
        for left_brick, right_brick in zip(left_wall, right_wall):
            x_position = right_brick.rect.x - self.grid_dimensions[0] + (TILE_WIDTH_PIXELS * 2)
            y_position = right_brick.rect.y
            left_brick.rect.move_ip(x_position, y_position)
        for bottom_brick, top_brick in zip(bottom_wall, top_wall):
            x_position = top_brick.rect.x
            y_position = top_brick.rect.y + self.grid_dimensions[1] - (TILE_WIDTH_PIXELS * 2)
            bottom_brick.rect.move_ip(x_position, y_position)
        self.bricks = top_wall + right_wall + bottom_wall + left_wall

    def change_color(self, color):
        for brick in self.bricks:
            brick.image.fill(color, brick.image.get_rect().inflate(-8, -8))

    def draw(self, surface):
        for brick in self.bricks:
            surface.blit(brick.image, brick.rect)


class Brick():
    """A small square barrier. The game ends if the snake touches it."""
    def __init__(self, color):
        self.image = pygame.Surface((TILE_WIDTH_PIXELS * 2, TILE_WIDTH_PIXELS * 2)).convert()
        self.image.fill(BLACK)
        self.image.fill(color, self.image.get_rect().inflate(-8, -8))
        self.rect = self.image.get_rect()

    def move_to(self, x, y):
        self.rect.topleft = x, y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def change_color(self, color):
        self.image.fill(color, self.image.get_rect().inflate(-8, -8))