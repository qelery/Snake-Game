import os
import sys
import time
import pygame
from config import *


class StartMenu:
    """
    The start menu.

    A screen where the player configures the game's difficulty, snake color, and grid size.
    Shows the game's directions after the settings are locked in.

    Methods
    -------
    get_users_settings()
        allow the user to chose the difficulty, snake color, and grid size
    show_directions()
        show the game's directions
    """
    def __init__(self, window_dimensions, screen):
        self.border_color = MEDIUM_GRAY
        self.window_dimensions = window_dimensions
        self.screen = screen

        self.background_image = pygame.Surface(self.window_dimensions).convert()
        self.background_image.fill(DARK_GRAY)
        self.background_rect = self.background_image.get_rect()
        self.background_image.fill(self.border_color, self.background_image.get_rect().inflate(-25, -25))

        self.font_xsmall = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_XSMALL)
        self.font_small = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_SMALL)
        self.font_medium = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_MEDIUM)
        self.font_large = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_LARGE)
        self.font_huge = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_HUGE)

        self.settings_text = self.font_large.render("SETTINGS", True, DARK_GRAY, self.border_color)
        self.settings_text_rect = self.settings_text.get_rect()
        self.settings_text_rect.center = (self.window_dimensions[0] * 0.5, self.window_dimensions[1] * 0.10)

        self.tile_size_text = self.font_small.render("Difficulty", True, DARK_GRAY, self.border_color)
        self.tile_size_text_rect = self.tile_size_text.get_rect()
        self.tile_size_text_rect.topleft = (self.window_dimensions[0] * 0.05, self.window_dimensions[1] * 0.25)

        self.snake_color_text = self.font_small.render("Snake Color", True, DARK_GRAY, self.border_color)
        self.snake_color_text_rect = self.snake_color_text.get_rect()
        self.snake_color_text_rect.topleft = (self.window_dimensions[0] * 0.05, self.window_dimensions[1] * 0.47)

        self.grid_size_text = self.font_small.render("Grid Size", True, DARK_GRAY, self.border_color)
        self.grid_size_text_rect = self.grid_size_text.get_rect()
        self.grid_size_text_rect.topleft = (self.window_dimensions[0] * 0.05, self.window_dimensions[1] * 0.69)

        self.go_text = self.font_huge.render("GO", True, DARK_GRAY, self.border_color)
        self.go_text_rect = self.go_text.get_rect()
        self.go_text_rect.center = (self.window_dimensions[0] * 0.85, self.window_dimensions[1] * 0.89)

        self.press_enter_text = self.font_large.render("Press Enter", True, DARK_GRAY, self.border_color)
        self.press_enter_text_rect = self.press_enter_text.get_rect()
        self.press_enter_text_rect.center = (self.window_dimensions[0] * 0.50, self.window_dimensions[1] * 0.89)

        fullname = os.path.join('images/', 'arrow_keys_small.png')
        self.arrow_keys_image = pygame.image.load(fullname).convert()
        color_key = self.arrow_keys_image.get_at((0, 0))
        self.arrow_keys_image.set_colorkey(color_key, pygame.RLEACCEL)
        self.arrow_keys_image = pygame.transform.scale(self.arrow_keys_image,
                                                       (int(self.arrow_keys_image.get_width() * 0.55),
                                                        int(self.arrow_keys_image.get_height() * 0.55)))
        self.arrow_keys_rect = self.arrow_keys_image.get_rect()
        self.arrow_keys_rect.center = (self.window_dimensions[0] * 0.8, self.window_dimensions[1] * 0.15)

        self.chime_low = pygame.mixer.Sound(SOUND_PATH + CHIME_LOW_SOUND)
        self.chime_high = pygame.mixer.Sound(SOUND_PATH + CHIME_HIGH_SOUND)
        self.blip = pygame.mixer.Sound(SOUND_PATH + DING_SOUND)

        self.difficulty_choices = [
            DifficultyModel(self.window_dimensions,
                            game_speed=40,
                            snake_elongation_rate=6,
                            name="Normal"),
            DifficultyModel(self.window_dimensions,
                            game_speed=44,
                            snake_elongation_rate=8,
                            name="Hard"),
            DifficultyModel(self.window_dimensions,
                            game_speed=50,
                            snake_elongation_rate=12,
                            name="Brutal"),
            DifficultyModel(self.window_dimensions,
                            game_speed=38,
                            snake_elongation_rate=4,
                            name="Easy"),
        ]

        self.snake_color_choices = [
            SnakeColorsGraphic(self.window_dimensions, BLUE_SPECTRUM),
            SnakeColorsGraphic(self.window_dimensions, GREEN_SPECTRUM),
            SnakeColorsGraphic(self.window_dimensions, PURPLE_SPECTRUM),
        ]

        # grid size lengths must be an even integer
        self.grid_dimensions_choices = [
            GridDimensionsGraphic(self.window_dimensions, 38, 38),
            GridDimensionsGraphic(self.window_dimensions, 56, 56),
            GridDimensionsGraphic(self.window_dimensions, 90, 44),
            GridDimensionsGraphic(self.window_dimensions, 36, 56),
            GridDimensionsGraphic(self.window_dimensions, 26, 26),
        ]

        self.settings = [0, 0, 0, 0]
        self.currently_selected_setting = 0
        self._highlight_selection()

        self.final_game_speed = None
        self.final_snake_elongation_factor = None
        self.final_snake_color = None
        self.final_grid_dimensions = None

    def get_users_settings(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key in [K_w, K_UP, K_s, K_DOWN]:
                    self._toggle_between_settings(event.key)
                elif event.type == KEYDOWN and event.key in [K_a, K_LEFT, K_d, K_RIGHT]:
                    self._toggle_between_setting_choices(event.key)
                elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_KP_ENTER):
                    was_submitted = self._try_to_submit()
                    if was_submitted:
                        self.blip.play()
                        time.sleep(0.5)
                        return (
                            self.final_game_speed,
                            self.final_snake_color,
                            self.final_snake_elongation_factor,
                            self.final_grid_dimensions,
                        )
            self._draw()
            pygame.display.flip()

    def show_directions(self):
        directions_text = self.font_huge.render("Directions", True, DARK_GRAY, self.border_color)
        directions_text_rect = directions_text.get_rect()
        directions_text_rect.center = (self.window_dimensions[0] * 0.5, self.window_dimensions[1] * 0.12)

        controls_text = self.font_medium.render("Controls", True, DARK_GRAY, self.border_color)
        controls_text_rect = controls_text.get_rect()
        controls_text_rect.center = (self.window_dimensions[0] * 0.5, self.window_dimensions[1] * 0.25)

        or_text = self.font_small.render("or", True, DARK_GRAY, self.border_color)
        or_text_rect = or_text.get_rect()
        or_text_rect.center = (self.window_dimensions[0] * 0.5, self.window_dimensions[1] * 0.37)

        press_any_key_text = self.font_medium.render("Press any key to continue", True, DARK_GRAY, self.border_color)
        press_any_key_text_rect = press_any_key_text.get_rect()
        press_any_key_text_rect.center = (self.window_dimensions[0] * 0.5, self.window_dimensions[1] * 0.9)

        red_apple_image = pygame.Surface((25, 25)).convert()
        red_apple_rect = red_apple_image.fill(RED)
        red_apple_rect.center = (self.window_dimensions[0] * 0.39, self.window_dimensions[1] * 0.525)
        red_apple_text = f"Red apples {'':>6} grow the snake slightly"
        red_apple_text = self.font_xsmall.render(red_apple_text, True, DARK_GRAY, self.border_color)
        red_apple_text_rect = red_apple_text.get_rect()
        red_apple_text_rect.center = (self.window_dimensions[0] * 0.50, self.window_dimensions[1] * 0.525)

        poison_apple_image = pygame.Surface((25, 25)).convert()
        poison_apple_rect = poison_apple_image.fill(POISON)
        poison_apple_rect.center = (self.window_dimensions[0] * 0.42, self.window_dimensions[1] * 0.625)
        poison_apple_text = f"Poison apples {'':>6} grow the snake rapidly"
        poison_apple_text = self.font_xsmall.render(poison_apple_text,True, DARK_GRAY, self.border_color)
        poison_apple_text_rect = poison_apple_text.get_rect()
        poison_apple_text_rect.center = (self.window_dimensions[0] * 0.50, self.window_dimensions[1] * 0.625)

        golden_apple_image = pygame.Surface((25, 25)).convert()
        golden_apple_rect = golden_apple_image.fill(GOLDEN)
        golden_apple_rect.center = (self.window_dimensions[0] * 0.48, self.window_dimensions[1] * 0.725)
        golden_apple_text = f"Golden apples {'':>6} shrink the snake"
        golden_apple_text = self.font_xsmall.render(golden_apple_text, True, DARK_GRAY, self.border_color)
        golden_apple_text_rect = golden_apple_text.get_rect()
        golden_apple_text_rect.center = (self.window_dimensions[0] * 0.50, self.window_dimensions[1] * 0.725)

        fullname = os.path.join('images/', 'wasd_keys_small.png')
        wasd_keys_image = pygame.image.load(fullname).convert_alpha()
        wasd_keys_image = pygame.transform.smoothscale(wasd_keys_image, (
            int(wasd_keys_image.get_width() * .50), int(wasd_keys_image.get_height() * .50)))
        wasd_keys_rect = wasd_keys_image.get_rect()
        wasd_keys_rect.center = (self.window_dimensions[0] * 0.25, self.window_dimensions[1] * 0.32)

        fullname = os.path.join('images/', 'arrow_keys_small.png')
        arrow_keys_image = pygame.image.load(fullname).convert_alpha()
        color_key = self.arrow_keys_image.get_at((0, 0))
        arrow_keys_image.set_colorkey(color_key, pygame.RLEACCEL)
        arrow_keys_image = pygame.transform.smoothscale(arrow_keys_image, (
            int(arrow_keys_image.get_width() * .60), int(arrow_keys_image.get_height() * .60)))
        arrow_keys_rect = arrow_keys_image.get_rect()
        arrow_keys_rect.center = (self.window_dimensions[0] * 0.75, self.window_dimensions[1] * 0.32)

        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(directions_text, directions_text_rect)
        self.screen.blit(controls_text, controls_text_rect)
        self.screen.blit(or_text, or_text_rect)
        self.screen.blit(wasd_keys_image, wasd_keys_rect)
        self.screen.blit(arrow_keys_image, arrow_keys_rect)
        self.screen.blit(press_any_key_text, press_any_key_text_rect)
        self.screen.blit(red_apple_text, red_apple_text_rect)
        self.screen.blit(red_apple_image, red_apple_rect)
        self.screen.blit(poison_apple_text, poison_apple_text_rect)
        self.screen.blit(poison_apple_image, poison_apple_rect)
        self.screen.blit(golden_apple_text, golden_apple_text_rect)
        self.screen.blit(golden_apple_image, golden_apple_rect)
        pygame.display.flip()

    def _toggle_between_settings(self, command):
        self.chime_low.play()
        if command in [K_s, K_DOWN]:
            self.currently_selected_setting += 1
            self._highlight_selection()
        else:
            self.currently_selected_setting -= 1
            self._highlight_selection()

    def _toggle_between_setting_choices(self, keypress):
        self.chime_high.play()
        if keypress in [K_a, K_LEFT]:
            self.settings[self.currently_selected_setting % len(self.settings)] -= 1
        else:
            self.settings[self.currently_selected_setting % len(self.settings)] += 1

    def _try_to_submit(self):
        if self.currently_selected_setting % len(self.settings) == 3:
            self.final_game_speed = self.difficulty_choices[self.settings[0] % len(self.difficulty_choices)].clock_speed

            self.final_snake_color = self.snake_color_choices[self.settings[1] % len(self.snake_color_choices)].color
            self.final_grid_dimensions = self.grid_dimensions_choices[
                self.settings[2] % len(self.grid_dimensions_choices)].dimensions

            elongation_rate = self.difficulty_choices[self.settings[0] % len(self.difficulty_choices)].snake_elongation_rate
            self.final_snake_elongation_factor = int(
                self.final_grid_dimensions[0] * self.final_grid_dimensions[1] / (38 * 38) * elongation_rate)

            return True

    def _highlight_selection(self):
        if self.currently_selected_setting % len(self.settings) == 0:
            self.go_text = self.font_huge.render("GO", True, DARK_GRAY, self.border_color)
            self.tile_size_text = self.font_small.render("Difficulty", True, GOLDEN, self.border_color)
            self.snake_color_text = self.font_small.render("Snake Color", True, DARK_GRAY, self.border_color)
        elif self.currently_selected_setting % len(self.settings) == 1:
            self.tile_size_text = self.font_small.render("Difficulty", True, DARK_GRAY, self.border_color)
            self.snake_color_text = self.font_small.render("Snake Color", True, GOLDEN, self.border_color)
            self.grid_size_text = self.font_small.render("Grid Size", True, DARK_GRAY, self.border_color)
        elif self.currently_selected_setting % len(self.settings) == 2:
            self.snake_color_text = self.font_small.render("Snake Color", True, DARK_GRAY, self.border_color)
            self.grid_size_text = self.font_small.render("Grid Size", True, GOLDEN, self.border_color)
            self.go_text = self.font_huge.render("GO", True, DARK_GRAY, self.border_color)
        elif self.currently_selected_setting % len(self.settings) == 3:
            self.grid_size_text = self.font_small.render("Grid Size", True, DARK_GRAY, self.border_color)
            self.go_text = self.font_huge.render("GO", True, GOLDEN, self.border_color)
            self.tile_size_text = self.font_small.render("Difficulty", True, DARK_GRAY, self.border_color)

    def _draw(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.settings_text, self.settings_text_rect)
        self.screen.blit(self.tile_size_text, self.tile_size_text_rect)
        self.screen.blit(self.snake_color_text, self.snake_color_text_rect)
        self.screen.blit(self.grid_size_text, self.grid_size_text_rect)
        self.screen.blit(self.go_text, self.go_text_rect)
        self.screen.blit(self.arrow_keys_image, self.arrow_keys_rect)
        if self.currently_selected_setting % len(self.settings) == 3:
            self.screen.blit(self.press_enter_text, self.press_enter_text_rect)

        tile_model = self.difficulty_choices[self.settings[0] % len(self.difficulty_choices)]
        self.screen.blit(tile_model.text, tile_model.rect)

        snake_model = self.snake_color_choices[self.settings[1] % len(self.snake_color_choices)]
        for image, rect in zip(snake_model.segment_images, snake_model.segment_rects):
            self.screen.blit(image, rect)

        grid_model = self.grid_dimensions_choices[self.settings[2] % len(self.grid_dimensions_choices)]
        self.screen.blit(grid_model.image, grid_model.rect)


class DifficultyModel:
    """A text graphic representing the different game difficulties the player can chose from."""
    def __init__(self, window_dimensions, game_speed, snake_elongation_rate, name):
        self.clock_speed = game_speed
        self.snake_elongation_rate = snake_elongation_rate
        self.name = name
        self.font_medium = pygame.font.Font(FONT_PATH + STANDARD_FONT, FONT_SIZE_SMALL)
        self.text = self.font_medium.render(name, True, DARK_GRAY, (246, 253, 255))
        self.rect = self.text.get_rect()
        self.rect.center = (window_dimensions[0] * 0.50, window_dimensions[1] * 0.28)


class SnakeColorsGraphic:
    """A snake graphic showcasing the snake colors the player can chose from."""
    def __init__(self, window_dimensions, color):
        self.color = color
        self.segment_images = [pygame.Surface((15, 15)).convert() for i in range(11)]
        for image in self.segment_images[:-1]:
            image.fill(color())
        self.segment_rects = [image.get_rect() for image in self.segment_images]
        x_pos = window_dimensions[0] * 0.42
        y_pos = window_dimensions[1] * 0.52
        self.segment_rects[0].move_ip(x_pos, y_pos)
        self.segment_rects[1].move_ip(x_pos + 15, y_pos)
        self.segment_rects[2].move_ip(x_pos + 30, y_pos)
        self.segment_rects[3].move_ip(x_pos + 45, y_pos)
        self.segment_rects[4].move_ip(x_pos + 45, y_pos - 15)
        self.segment_rects[5].move_ip(x_pos + 45, y_pos - 30)
        self.segment_rects[6].move_ip(x_pos + 45, y_pos - 45)
        self.segment_rects[7].move_ip(x_pos + 45, y_pos - 60)
        self.segment_rects[8].move_ip(x_pos + 60, y_pos - 60)
        self.segment_rects[9].move_ip(x_pos + 75, y_pos - 60)
        self.segment_rects[10].move_ip(x_pos + 90, y_pos - 60)


class GridDimensionsGraphic:
    """A graphic showcasing the sizes and shapes of the grids the player can chose from."""
    def __init__(self, window_dimensions, width, length):
        self.dimensions = (width, length)
        self.image = pygame.Surface((int(width * 2), int(length * 2))).convert()
        self.image.fill(LIGHT_GRAY, self.image.get_rect().inflate(-8, -8))
        self.rect = self.image.get_rect()
        self.rect.center = (window_dimensions[0] * 0.5, window_dimensions[1] * 0.72)
