import pygame
from config import *


class Snake:
    """
    The snake.

    Although the snake appears as a series of multicolored lines, it is actually a series of multicolored
    squares. The next square in the sequence is shoved two-thirds of the way under the square before it.
    This design choice was made because it causes the snake to partially fold onto itself when it turns.
    This produces a fluid flow of hues, almost like water.

    ...

    Attributes
    ----------
    color : function
        returns a random rgb hue tuple of it's function name; Ex: BLUE() returns random blue hues
    head : HeadPiece
        the head of the snake
    all_pieces : list of SnakePiece
        all segments of the snake
    body_pieces_only : list of SnakePiece
        all segments of the snake except the head
    initial_elongation_factor : int
        before any level ups, how cycles the snake will elongate for when triggered to grow
    elongation_factor : int
        the current number of cycles the snake will elongate for when triggered to grow
    elongation_cycles_remaining : int
        how many more cycle (pygame clock ticks) the snake will elongate for

    Methods
    -------
    spawn_snake_parts()
        add another segment onto the back of the snake
    remove_half()
        removes roughly half of the snake from the back end
    level_up()
        reset the snake back to just the head and increase its elongation factor
    """
    def __init__(self, color, elongation_factor):
        self.color = color
        self.head = HeadPiece()
        self.all_pieces = [self.head]
        self.body_pieces_only = []
        self.initial_elongation_factor = elongation_factor
        self.elongation_factor = elongation_factor
        self.elongation_cycles_remaining = 0

    def update(self):
        non_new_snake_pieces = self.all_pieces.copy()
        if self.elongation_cycles_remaining:
            self.elongation_cycles_remaining -= 1
            self.spawn_snake_part()
        for piece in reversed(self.body_pieces_only):
            piece.determine_next_position()
        for piece in non_new_snake_pieces:
            piece.move_to_next_position()

    def spawn_snake_part(self):
        if len(self.all_pieces) < 3:
            color = BLACK
        else:
            color = self.color()
        new_body_part = BodyPiece(previous_piece=self.all_pieces[-1], color=color)
        self.all_pieces.append(new_body_part)
        self.body_pieces_only.append(new_body_part)

    def remove_half(self):
        self.elongation_cycles_remaining = 0
        snake_body_len = len(self.body_pieces_only)
        if not snake_body_len:
            return
        if snake_body_len <= self.elongation_factor:
            del self.all_pieces[-snake_body_len:]
            del self.body_pieces_only[-snake_body_len:]
        else:
            half_snake_len = int(snake_body_len / 2)
            amount_of_snake_to_remove = int(snake_body_len - half_snake_len)
            del self.all_pieces[-amount_of_snake_to_remove:]
            del self.body_pieces_only[-amount_of_snake_to_remove:]

    def level_up(self):
        self.elongation_cycles_remaining = 0
        self.all_pieces = [self.head]
        self.body_pieces_only = []
        self.elongation_factor += self.initial_elongation_factor


class SnakePiece:
    def __init__(self):
        self.image = pygame.Surface((TILE_WIDTH_PIXELS, TILE_WIDTH_PIXELS)).convert()
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class HeadPiece(SnakePiece):
    def __init__(self):
        super().__init__()
        self.image.fill(BLACK)
        self.rect.topleft = 0, 0
        self.moveX = 0
        self.moveY = 0
        self.speed = PIXELS_TRAVERSED_PER_UPDATE
        self.command_pending = None

    def move_to(self, x, y):
        self.rect.topleft = x, y

    def move_to_next_position(self):
        self._change_direction()
        self.rect.move_ip(self.moveX, self.moveY)

    def _change_direction(self):
        # First line ensures snake only executes directional change command along predefined grid pattern
        if (self.rect.topleft[0] % TILE_WIDTH_PIXELS == 0) and ((self.rect.topleft[1] - 100) % TILE_WIDTH_PIXELS == 0):
            if self.command_pending:
                if not self.moveX:
                    if self.command_pending in [K_a, K_LEFT]:
                        self.moveY = 0
                        self.moveX = -self.speed
                        return
                    elif self.command_pending in [K_d, K_RIGHT]:
                        self.moveY = 0
                        self.moveX = self.speed
                        return
                if not self.moveY:
                    if self.command_pending in [K_s, K_DOWN]:
                        self.moveX = 0
                        self.moveY = self.speed
                        return
                    elif self.command_pending in [K_w, K_UP]:
                        self.moveX = 0
                        self.moveY = -self.speed
                        return


class BodyPiece(SnakePiece):
    def __init__(self, previous_piece, color):
        super().__init__()
        self.previous_piece = previous_piece
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.moveX = self.previous_piece.moveX
        self.moveY = self.previous_piece.moveY
        self.rect.topleft = self.previous_piece.rect.topleft

    def determine_next_position(self):
        self.moveX = self.previous_piece.moveX
        self.moveY = self.previous_piece.moveY

    def move_to_next_position(self):
        self.rect.move_ip(self.moveX, self.moveY)
