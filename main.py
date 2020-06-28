import sys
import time
import pygame

from config import *
from startmenu import StartMenu
from grid import Grid
from statsbanner import StatsBanner
from snake import Snake


class Game:
    """"
    Snake game.

    Move the snake to collect apples, score points, and level up. 10 levels total.

    ...

    Attributes
    ----------
    window_dimensions : tuple of int
        dimension in pixels of the game window
    screen : pygame.Surface
        the surface on which all of the game's sprites are displayed
    start_menu : StartMenu
        the game's start menu
    clock_speed : int
        the game's frame rate
    stats_banner : StatsBanner
        displays the points and current level
    grid : Grid
        the board on which the game is played
    color_palettes : tuple of tuple
        tuples of rgb color values

    Methods
    -------
    play()
        the main loop of the game

    """

    def __init__(self):
        pygame.display.set_caption("SNAKE by Qelery")
        pygame.mouse.set_visible(False)
        self.window_dimensions = DEFAULT_WINDOW_DIMENSIONS
        self.screen = pygame.display.set_mode(self.window_dimensions)
        self.start_menu = StartMenu(self.window_dimensions, self.screen)
        self.clock_speed = 0
        self.stats_banner = None
        self.grid = None
        self.color_palettes = (
            GREEN_PALETTE,
            RED_PALETTE,
            BLUE_PALETTE,
            BROWN_PALETTE,
            PURPLE_PALETTE,
        )

    def play(self):
        self._run_start_menu()
        clock = pygame.time.Clock()
        self.stats_banner.announce_level_change()

        while True:
            clock.tick(self.clock_speed)
            self._handle_input_events()
            self._update()
            self._draw()
            self._checks()
            pygame.display.flip()
            if self.grid.check_snake_collision():
                self._game_lost()
                break

    def _update(self):
        self.stats_banner.update()
        self.grid.update()

    def _draw(self):
        self.grid.draw(self.screen)
        self.stats_banner.draw(self.screen)
        pygame.display.flip()

    def _checks(self):
        is_collision = self.grid.check_apple_eaten()
        if is_collision:
            self.stats_banner.score += 1
            if self.stats_banner.score == POINTS_PER_LEVEL:
                self._update_level()

    def _run_start_menu(self):
        settings = self.start_menu.get_users_settings()
        self.clock_speed = settings[0]
        snake = Snake(settings[1], settings[2])
        dimensions = (settings[3][0] * TILE_WIDTH_PIXELS, settings[3][1] * TILE_WIDTH_PIXELS)
        self.grid = Grid(dimensions, GREEN_PALETTE, snake)
        self.window_dimensions = self.grid.dimensions[0], self.grid.dimensions[1] + BANNER_DIMENSIONS[1]
        self.stats_banner = StatsBanner(self.grid.dimensions, GREEN_PALETTE[2])
        self.start_menu.show_directions()
        wait_for_keypress()
        self.screen = pygame.display.set_mode((self.grid.dimensions[0], self.grid.dimensions[1] + BANNER_DIMENSIONS[1]))

    def _update_level(self):
        if self.stats_banner.level == 10:
            self._game_won()
        self.grid.level_up()
        self.stats_banner.level += 1
        self.stats_banner.score = 0
        self.stats_banner.announce_level_change()

        if self.stats_banner.level == 10:  # final level
            self.grid.snake.color = YARN_COLOR
            palette = GREY_PALETTE
        else:
            palette = self.color_palettes[(self.stats_banner.level - 1) % len(self.color_palettes)]
        self.grid.change_color(palette[0], palette[1])
        self.stats_banner.change_color(palette[2])

    def _handle_input_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key in ARROW_KEYS:
                self.grid.snake.head.command_pending = event.key

    def _game_lost(self):
        pygame.mixer.Sound(SOUND_PATH + LOSS_SOUND).play()
        time.sleep(3.5)

        font_huge = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_HUGE)
        font_large = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_LARGE)

        you_lost_text = font_huge.render("YOU LOST", True, DARK_GRAY)
        you_lost_rect = you_lost_text.get_rect()
        you_lost_rect.center = self.grid.dimensions[0] * 0.5, (self.grid.dimensions[1] * 0.45) + BANNER_DIMENSIONS[1]

        play_again_text = font_large.render("Play again? Y / N", True, DARK_GRAY)
        play_again_rect = play_again_text.get_rect()
        play_again_rect.center = self.grid.dimensions[0] * 0.5, (self.grid.dimensions[1] * 0.55) + BANNER_DIMENSIONS[1]

        self.screen.blit(you_lost_text, you_lost_rect)
        self.screen.blit(play_again_text, play_again_rect)
        pygame.display.flip()

    def _game_won(self):
        pygame.mixer.Sound(SOUND_PATH + VICTORY_SOUND).play()
        font_huge = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_HUGE)
        text = font_huge.render("YOU WON!", True, DARK_GRAY)
        text_rect = text.get_rect()
        text_rect.center = self.grid.dimensions[0] * 0.5, (self.grid.dimensions[1] * 0.5) + BANNER_DIMENSIONS[1]
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)
        wait_for_keypress()
        pygame.quit()
        sys.exit()


def prompt_play_again():
    clock = pygame.time.Clock()
    pygame.event.clear()
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_y:
                return True
            elif event.type == KEYDOWN and event.key == K_n:
                return False


def wait_for_keypress():
    clock = pygame.time.Clock()
    pygame.event.clear()
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return


if __name__ == '__main__':
    pygame.init()
    if not pygame.font: print("Was not able to initialize fonts.")
    if not pygame.mixer: print("Was not able to initialize sounds.")
    while True:
        game = Game()
        game.play()
        play_again = prompt_play_again()
        if not play_again:
            pygame.quit()
            break
