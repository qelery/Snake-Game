import pygame
from config import *
from apple import Apple
from wall import BrickWall


class Grid:
    """
    A rectangular grid on which the game is played.

    ...

    Attributes
    ----------
    dimensions : tuple of int
        the dimensions of the playing grid in pixels
    background : pygame.Surface
        a rectangular graphic representing the grid
    rect : pygame.Rect
        coordinates of the grid
    snake : Snake
        the single snake in the game
    red_apple : Apple
        the single apple in the game
    other_apples : list of Apple
        a collection of golden and poison currently on the grid
    other_apple_spawn_rate : float
        the rate at which golden and poison apples randomly spawn onto grid
    other_apple_despawn_rate : float
        the rate at which golden and poison apples are randomly removed from the grid

    Methods
    -------
    randomly_place_sprite(sprite_to_place)
        randomly place sprite on grid where it will not overlap with the snake, any apples, or the wall
    check_apple_eaten()
        handle events for when the snake runs into an apple
    check_snake_collision()
        handle events for when the snake runs into a wall or itself
    level_up()
        change the snake and apple stats when the player levels up
    update()
        update the grid's snake and randomly spawn apples
    change_colors()
        change the colors of the grid's background and wall
    draw()
        draw the grid and it's snake and apples to the screen
    """
    def __init__(self, dimensions, color_palette, snake):
        self.dimensions = dimensions
        self.background = pygame.Surface(dimensions).convert()
        self.background.fill(color_palette[0])
        self.rect = self.background.get_rect()
        self.rect.topleft = 0, BANNER_DIMENSIONS[1]
        self.brick_wall = BrickWall(self.dimensions, color_palette[1])
        self.snake = snake
        self.red_apple = Apple(RED)
        self.other_apples = []
        self.other_apple_spawn_rate = 0.0050
        self.other_apple_despawn_rate = 0.0025
        self.randomly_place_sprite(self.snake.head)
        self.randomly_place_sprite(self.red_apple)

    def randomly_place_sprite(self, sprite_to_place):
        while True:
            rows_in_grid = int(self.dimensions[1] / TILE_WIDTH_PIXELS)
            columns_in_grid = int(self.dimensions[0] / TILE_WIDTH_PIXELS)
            x_pos = random.randint(0, columns_in_grid - 1) * TILE_WIDTH_PIXELS
            y_pos = random.randint(0, rows_in_grid - 1) * TILE_WIDTH_PIXELS + BANNER_DIMENSIONS[1]
            sprite_to_place.move_to(x_pos, y_pos)
            all_sprites = (self.snake.all_pieces +
                           self.other_apples +
                           self.brick_wall.bricks)
            all_other_sprites = [sprite for sprite in all_sprites if sprite is not sprite_to_place]
            if sprite_to_place.rect.collidelist(all_other_sprites) == -1 and self.rect.contains(sprite_to_place.rect):
                return

    def check_apple_eaten(self):
        all_apples = self.other_apples + [self.red_apple]
        collision_index = self.snake.head.rect.collidelist(all_apples)
        if collision_index != -1:  # if collision
            apple_obtained = all_apples[collision_index]
            apple_obtained.eaten_sound.play()
            if apple_obtained.color == RED:
                self.randomly_place_sprite(self.red_apple)
                self.snake.elongation_cycles_remaining += self.snake.elongation_factor
            elif apple_obtained.color == GOLDEN:
                self.snake.remove_half()
                del self.other_apples[collision_index]
            elif apple_obtained.color == POISON:
                self.snake.elongation_cycles_remaining += self.snake.elongation_factor * 5
                del self.other_apples[collision_index]
            return True
        return False

    def check_snake_collision(self):
        # ignore first 5 pieces of snake body, they overlap with snake's head when turning
        if self.snake.head.rect.collidelist(self.snake.body_pieces_only[5:]) != -1:
            return True
        if self.snake.head.rect.collidelist(self.brick_wall.bricks) != -1:
            return True
        return False

    def level_up(self):
        self.snake.level_up()
        self.other_apples = []
        self.other_apple_spawn_rate *= 1.05
        self.other_apple_despawn_rate *= 1.05

    def update(self):
        self.snake.update()
        self._handle_snake_OOB()
        self._apple_spawn_events()

    def change_color(self, background_color, wall_color):
        self.background.fill(background_color)
        self.brick_wall.change_color(wall_color)

    def draw(self, surface):
        surface.blit(self.background, self.rect)
        self.red_apple.draw(surface)
        for apple in self.other_apples:
            apple.draw(surface)
        for piece in self.snake.all_pieces:
            piece.draw(surface)
        self.brick_wall.draw(surface)

    def _handle_snake_OOB(self):
        for piece in self.snake.all_pieces:
            if piece.rect.right > self.rect.right:
                piece.rect.move_ip(-self.dimensions[0], 0)
                return
            elif piece.rect.left < self.rect.left:
                piece.rect.move_ip(+self.dimensions[0], 0)
                return
            elif piece.rect.top < self.rect.top:
                piece.rect.move_ip(0, +self.dimensions[1])
                return
            elif piece.rect.bottom > self.rect.bottom:
                piece.rect.move_ip(0, -self.dimensions[1])
                return

    def _apple_spawn_events(self):
        if random.random() < self.other_apple_spawn_rate:
            if random.random() < 0.1:
                self.other_apples.append(Apple(GOLDEN))
            else:
                self.other_apples.append(Apple(POISON))
            self.randomly_place_sprite(self.other_apples[-1])
        if random.random() < self.other_apple_despawn_rate and self.other_apples:
            apple_to_delete = random.choice(self.other_apples)
            self.other_apples.remove(apple_to_delete)


