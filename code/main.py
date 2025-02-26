import pygame
import sys
import time
import shutil  
import os
import settings as game_settings
from level import *
from PIL import Image, ImageSequence  
from debug import *

class Intro:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 60)
        self.text = "RPG ELDORIA"
        self.version_text = "v2.0.0"
        self.audio_manager = AudioManager() 

    def fade_to_black(self, delay=10, alpha_step=8): 
        fade_surface = pygame.Surface((WIDTH, HEIGTH))
        fade_surface.fill((0, 0, 0)) 
        for alpha in range(0, 256, alpha_step): 
            fade_surface.set_alpha(alpha)
            self.screen.fill(WATER_COLOR)  
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(delay)

    def fade_in(self, delay=10, alpha_step=8):
        fade_surface = pygame.Surface((WIDTH, HEIGTH))
        fade_surface.fill((0, 0, 0))  
        for alpha in range(255, -1, -alpha_step):  
            fade_surface.set_alpha(alpha)
            self.screen.fill(WATER_COLOR)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(delay)
            
    def type_text(self, text, color, center_x, center_y, delay=0.05): 
        displayed_text = ""
        for char in text:
            displayed_text += char
            rendered_text = self.font.render(displayed_text, True, color)
            text_rect = rendered_text.get_rect(center=(center_x, center_y))
            self.screen.fill(WATER_COLOR)  
            self.screen.blit(rendered_text, text_rect)
            pygame.display.flip()
            time.sleep(delay)  

    def display(self):
        self.audio_manager.play_music("../audio/main_intro.ogg", loops=-1, volume=0.5)  
        self.screen.fill((0, 0, 0)) 
        pygame.display.flip()
        time.sleep(0.5)  

        self.fade_in(delay=10, alpha_step=8) 

        self.type_text(self.text, TEXT_COLOR, WIDTH // 2, HEIGTH // 2, delay=0.05)  
        time.sleep(1)  

        self.fade_to_black(delay=10, alpha_step=8)  

        self.fade_in(delay=10, alpha_step=8) 

        self.type_text(self.version_text, TEXT_COLOR, WIDTH // 2, HEIGTH // 2, delay=0.05)  
        time.sleep(1)  

        self.fade_to_black(delay=10, alpha_step=8) 

        time.sleep(0.5) 
        self.audio_manager.stop_music()

class MainMenu:
    shared_background_frames = None # gif frames

    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(UI_FONT, 60)
        self.font_options = pygame.font.Font(UI_FONT, 40)
        self.title = "RPG ELDORIA"
        self.options = ["New Game", "Settings", "Quit Game"]
        self.selected_option = 0
        self.audio_manager = AudioManager()
        self.load_background_frames()
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()

        self.screen.blit(self.background_frames[self.current_frame], (0, 0))
        pygame.display.update()

    def load_background_frames(self):
        if MainMenu.shared_background_frames is None:
            gif = Image.open('../graphics/background/background.gif')
            frames = []

            for frame in ImageSequence.Iterator(gif):
                img = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert_alpha()
                scaled_img = pygame.transform.scale(img, (WIDTH, HEIGTH))
                frames.append(scaled_img)

            frames = [frame for frame in frames if not self.is_white_frame(frame)]
            
            MainMenu.shared_background_frames = frames

        self.background_frames = MainMenu.shared_background_frames

    def is_white_frame(self, frame):
        avg_color = pygame.transform.average_color(frame)
        return avg_color == (255, 255, 255, 255)  

    def display(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > 90:
            self.current_frame = (self.current_frame + 1) % len(self.background_frames)
            self.last_frame_time = current_time

        # Garante que o fundo não pisque branco
        self.screen.blit(self.background_frames[self.current_frame], (0, 0))

        # Render title
        title_surface = self.font_title.render(self.title, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGTH // 4))
        self.screen.blit(title_surface, title_rect)

        # Render menu options
        for i, option in enumerate(self.options):
            color = TEXT_COLOR if i != self.selected_option else "blue"
            option_surface = self.font_options.render(option, True, color)
            option_rect = option_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 + i * 50))
            self.screen.blit(option_surface, option_rect)

        pygame.display.update()

    def navigate(self, direction):
        self.selected_option = (self.selected_option + direction) % len(self.options)

    def select(self):
        if self.selected_option == 0:
            self.audio_manager.play_sound("../audio/menu/Menu1.wav", volume=2.5)
            return "new_game"
        elif self.selected_option == 1:
            self.audio_manager.play_sound("../audio/menu/Menu1.wav", volume=2.5)
            return "settings"
        elif self.selected_option == 2:
            self.audio_manager.play_sound("../audio/menu/Menu6.wav", volume=2.5)
            time.sleep(1)
            pygame.quit()
            sys.exit()

        return None


class Settings:
    def __init__(self):
        self.options = [
            {"name": "Fullscreen", "type": "toggle", "value": True},  # Default to fullscreen
            {"name": "Borderless", "type": "toggle", "value": False},
            {"name": "Resolution", "type": "choice", "choices": [(1280, 720), (1920, 1080), (800, 600), (1024, 768), (1280, 720), (1366, 768)], "value": 1},  # Default to 1920x1080
            {"name": "Game", "type": "choice", "choices": ["optimized", "normal", "extreme performance"], "value": 1},  # Default to normal
            {"name": "Gamma", "type": "slider", "min": 50, "max": 150, "value": 100},  # Gamma slider
            {"name": "Back", "type": "action"}
        ]
        self.selected = 0

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def toggle_option(self):
        option = self.options[self.selected]

        if option["type"] == "toggle":
            option["value"] = not option["value"]
            if option["name"] == "Fullscreen" and option["value"]:
                self.set_option("Borderless", False)

            elif option["name"] == "Borderless" and option["value"]:
                self.set_option("Fullscreen", False)

            return option["name"], option["value"]

        elif option["type"] == "choice":
            option["value"] = (option["value"] + 1) % len(option["choices"])
            return option["name"], option["choices"][option["value"]]

        elif option["type"] == "action" and option["name"] == "Back":
            return "Back", None

        return None, None

    def set_option(self, name, value):
        for opt in self.options:
            if opt["name"] == name:
                opt["value"] = value
                break

    def adjust_gamma(self, direction):
        option = self.options[self.selected]
        if option["type"] == "slider":
            option["value"] = max(option["min"], min(option["max"], option["value"] + direction))
            return option["name"], option["value"]
        return None, None

class MainMenuSettings:
    def __init__(self, screen, settings):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)  # Restore original font size
        self.settings = settings
        self.audio_manager = AudioManager()  

    def display(self):
        self.screen.fill(WATER_COLOR)
        for idx, option in enumerate(self.settings.options):
            color = TEXT_COLOR if idx == self.settings.selected else UI_BG_COLOR
            text = option["name"]
            
            if option["type"] == "toggle":
                text += f": {'On' if option['value'] else 'Off'}"
            elif option["type"] == "choice":
                current_res = option["choices"][option["value"]]
                text += f": {current_res[0]}x{current_res[1]}" if option["name"] == "Resolution" else f": {current_res}"
            elif option["type"] == "slider":
                text += f": {option['value']}"

            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)

        # Display buttons
        enter_img = pygame.image.load('../graphics/environment/sprite_buttons_menu/ENTER.png').convert_alpha()
        y_img = pygame.image.load('../graphics/environment/sprite_buttons_menu/Y.png').convert_alpha()
        esc_img = pygame.image.load('../graphics/environment/sprite_buttons_menu/ESC.png').convert_alpha()

        enter_img = pygame.transform.scale(enter_img, (20, 20))
        y_img = pygame.transform.scale(y_img, (20, 20))
        esc_img = pygame.transform.scale(esc_img, (20, 20))

        small_font = pygame.font.Font(UI_FONT, 20)
        enter_text = small_font.render("Toggle", True, BLACK_COLOR)
        y_text = small_font.render("Reset", True, BLACK_COLOR)
        esc_text = small_font.render("Back", True, BLACK_COLOR)

        self.screen.blit(enter_img, (WIDTH - 370, HEIGTH - 30))
        self.screen.blit(enter_text, (WIDTH - 340, HEIGTH - 30))
        self.screen.blit(y_img, (WIDTH - 230, HEIGTH - 30))
        self.screen.blit(y_text, (WIDTH - 200, HEIGTH - 30))
        self.screen.blit(esc_img, (WIDTH - 110, HEIGTH - 30))
        self.screen.blit(esc_text, (WIDTH - 80, HEIGTH - 30))

        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option:
            self.audio_manager.play_sound("../audio/menu/Menu9.wav", volume=2.5)
        return option, value

    def adjust_gamma(self, direction):
        option, value = self.settings.adjust_gamma(direction)
        if option:
            self.audio_manager.play_sound("../audio/menu/Menu9.wav", volume=2.5)
            self.apply_gamma(value)
        return option, value

    def apply_gamma(self, value):
        gamma = value / 100.0
        pygame.display.set_gamma(gamma)

    def reset_settings(self):
        fullscreen_before_reset = self.settings.options[0]["value"]
        self.settings = Settings()
        self.settings.set_option("Fullscreen", fullscreen_before_reset)
        if fullscreen_before_reset:
            self.settings.set_option("Borderless", False)
            game.toggle_fullscreen(borderless=False)
        else:
            game.toggle_fullscreen(borderless=True)

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)
        self.options = ["Resume Game", "Settings", "Quit Game"]
        self.selected = 0
        self.menu_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)  # Update to use SRCALPHA for transparency
        self.menu_surface.fill((0, 0, 0, 150))  # Fill with black color and set alpha
        self.audio_manager = AudioManager()  # => Add this line

    def display(self):
        self.menu_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)  # Update size to match current resolution
        self.menu_surface.fill((0, 0, 0, 150))  # Fill with black color and set alpha
        self.screen.blit(self.menu_surface, (0, 0))
        
        for idx, option in enumerate(self.options):
            color = TEXT_COLOR if idx == self.selected else UI_BG_COLOR
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(text, text_rect)
            
        pygame.display.flip()

    def navigate(self, direction):
        self.selected = (self.selected + direction) % len(self.options)

    def select(self):
        if self.selected == 0:  
            self.audio_manager.play_sound("../audio/menu/Menu1.wav", volume=2.5)
            return "resume"
        elif self.selected == 1:  
            self.audio_manager.play_sound("../audio/menu/Menu1.wav", volume=2.5)
            return "settings"
        elif self.selected == 2:  
            self.audio_manager.play_sound("../audio/menu/Menu6.wav", volume=2.5)
            time.sleep(0.5)
            return "quit"
        
class PauseMenuSettings:
    def __init__(self, screen, settings):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)  # Restore original font size
        self.settings = settings
        self.audio_manager = AudioManager()  

    def display(self):
        self.screen.fill(WATER_COLOR)
        
        for idx, option in enumerate(self.settings.options):
            color = TEXT_COLOR if idx == self.settings.selected else UI_BG_COLOR
            text = option["name"]
            
            if option["type"] == "toggle":
                text += f": {'On' if option['value'] else 'Off'}"
            elif option["type"] == "choice":
                current_res = option["choices"][option["value"]]
                text += f": {current_res[0]}x{current_res[1]}" if option["name"] == "Resolution" else f": {current_res}"
            elif option["type"] == "slider":
                text += f": {option['value']}"

            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)

        # Display buttons
        enter_img = pygame.image.load('../graphics/environment/sprite_buttons_menu/ENTER.png').convert_alpha()
        y_img = pygame.image.load('../graphics/environment/sprite_buttons_menu/Y.png').convert_alpha()
        esc_img = pygame.image.load('../graphics/environment/sprite_buttons_menu/ESC.png').convert_alpha()

        enter_img = pygame.transform.scale(enter_img, (20, 20))
        y_img = pygame.transform.scale(y_img, (20, 20))
        esc_img = pygame.transform.scale(esc_img, (20, 20))

        small_font = pygame.font.Font(UI_FONT, 20)
        enter_text = small_font.render("Toggle", True, BLACK_COLOR)
        y_text = small_font.render("Reset", True, BLACK_COLOR)
        esc_text = small_font.render("Back", True, BLACK_COLOR)

        self.screen.blit(enter_img, (WIDTH - 370, HEIGTH - 30))
        self.screen.blit(enter_text, (WIDTH - 340, HEIGTH - 30))
        self.screen.blit(y_img, (WIDTH - 230, HEIGTH - 30))
        self.screen.blit(y_text, (WIDTH - 200, HEIGTH - 30))
        self.screen.blit(esc_img, (WIDTH - 110, HEIGTH - 30))
        self.screen.blit(esc_text, (WIDTH - 80, HEIGTH - 30))

        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option:
            self.audio_manager.play_sound("../audio/menu/Menu9.wav", volume=2.5)
        return option, value

    def adjust_gamma(self, direction):
        option, value = self.settings.adjust_gamma(direction)
        if option:
            self.audio_manager.play_sound("../audio/menu/Menu9.wav", volume=2.5)
            self.apply_gamma(value)
        return option, value

    def apply_gamma(self, value):
        gamma = value / 100.0
        pygame.display.set_gamma(gamma)

    def reset_settings(self):
        fullscreen_before_reset = self.settings.options[0]["value"]
        self.settings = Settings()
        self.settings.set_option("Fullscreen", fullscreen_before_reset)
        if fullscreen_before_reset:
            self.settings.set_option("Borderless", False)
            game.toggle_fullscreen(borderless=False)
        else:
            game.toggle_fullscreen(borderless=True)

class AudioManager:
    def __init__(self):
        pygame.mixer.init() 

    #function for music
    def play_music(self, filename, loops=0, volume=0.5):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops)
        except pygame.error as e:
            pass
            #print(f"Error loading music: {filename}. Error: {e}")

    #function for effect 
    def play_sound(self, filename, volume=0.5):
        try:
            sound = pygame.mixer.Sound(filename)
            sound.set_volume(volume)
            sound.play()
        except pygame.error as e:
            pass
            #print(f"Error loading sound: {filename}. Error: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
        
        pygame.display.set_caption('RPG Eldoria')
        icon_path = '../graphics/icon/icon.game.data.ico'  
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.main_menu = MainMenu(self.screen)
        self.main_menu_settings = MainMenuSettings(self.screen, self.settings)
        self.pause_menu = PauseMenu(self.screen)
        self.pause_menu_settings = PauseMenuSettings(self.screen, self.settings)
        self.fullscreen = False
        self.in_menu = True
        self.in_settings = False
        self.in_pause = False
        self.in_pause_settings = False
        self.in_gameplay = False
        self.in_upgrade = False
        
        self.intro_played = False
        self.audio_manager = AudioManager()

        self.toggle_fullscreen()  

        if not self.intro_played:
            intro = Intro(self.screen)
            intro.display()
            self.intro_played = True

        self.audio_manager.play_music("../audio/main_menu.ogg", loops=-1, volume=0.5)
        self.apply_game_settings()

    def apply_game_settings(self):
        game_mode = self.settings.options[3]["value"]
        game_settings = {
            0: {"tilesize": 10,
                "chunksize": 10, 
                "visible_chunks": 1, 
                "wind_interval": 30000, "wind_duration": 5000,
                "max_wind": 1},
            
            1: {"tilesize": 25,
                "chunksize": 25,
                "visible_chunks": 5,
                "wind_interval": 20000, "wind_duration": 5000,
                "max_wind": 3},
            
            2: {"tilesize": 30,
                "chunksize": 30,
                "visible_chunks": 10,
                "wind_interval": 10000, "wind_duration": 5000,
                "max_wind": 5},
        }

        if game_mode in game_settings:
            self._apply_level_settings(game_settings[game_mode])
        else:
            #print(f"Game Mode Unknown: {game_mode}")
            pass

    def _apply_level_settings(self, config):
        self.level.clear_wind_effects()

        game_settings.TILESIZE = config["tilesize"]
        game_settings.CHUNKSIZE = config["chunksize"]
        game_settings.VISIBLE_CHUNKS = config["visible_chunks"]
        
        self.level.wind_effect_interval = config["wind_interval"]
        self.level.wind_effect_duration = config["wind_duration"]
        self.level.max_wind_effects = config["max_wind"]

        self.level.update_wind_effects_settings()
        self.level.spawn_wind_effects()
        
    def run(self):
        try:
            key_hold_time = 0
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if self.in_menu:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.main_menu.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.main_menu.navigate(1)
                            elif event.key == pygame.K_RETURN:
                                action = self.main_menu.select()
                                if action == "new_game":
                                    self.in_menu = False
                                    self.in_gameplay = True
                                    self.audio_manager.stop_music()
                                    self.audio_manager.play_music("../audio/main.ogg", loops=-1, volume=0.5)
                                elif action == "settings":
                                    self.in_menu = False
                                    self.in_settings = True
                                elif action == "quit":
                                    pygame.quit()
                                    sys.exit()
                                    del CHUNKS_FOLDER
                            elif event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()

                    elif self.in_pause:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.pause_menu.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.pause_menu.navigate(1)
                            elif event.key == pygame.K_RETURN:
                                action = self.pause_menu.select()
                                if action == "resume":
                                    self.in_pause = False
                                    self.audio_manager.stop_music()
                                    self.audio_manager.play_music("../audio/main.ogg", loops=-1, volume=0.5)
                                elif action == "settings":
                                    self.in_pause = False
                                    self.in_pause_settings = True
                                elif action == "quit":
                                    pygame.quit()
                                    sys.exit()
                                    del CHUNKS_FOLDER
                            elif event.key == pygame.K_ESCAPE:
                                self.in_pause = False
                                self.audio_manager.stop_music()
                                self.audio_manager.play_music("../audio/main.ogg", loops=-1, volume=0.5)

                    elif self.in_settings:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.main_menu_settings.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.main_menu_settings.navigate(1)
                            elif event.key == pygame.K_LEFT:
                                self.main_menu_settings.adjust_gamma(-1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RIGHT:
                                self.main_menu_settings.adjust_gamma(1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RETURN:
                                option, value = self.main_menu_settings.toggle_option()
                                if option == "Fullscreen":
                                    self.toggle_fullscreen(borderless=False)
                                elif option == "Borderless":
                                    self.toggle_fullscreen(borderless=True)
                                elif option == "Resolution":
                                    self.apply_resolution(value)
                                    self.settings.set_option("Fullscreen", False) 
                                elif option == "Back":
                                    self.in_settings = False
                                    self.in_menu = True
                            elif event.key == pygame.K_y:
                                fullscreen_before_reset = self.settings.options[0]["value"]
                                self.main_menu_settings.reset_settings()  
                                self.pause_menu_settings.reset_settings()  
                                self.settings.set_option("Fullscreen", fullscreen_before_reset)
                            elif event.key == pygame.K_ESCAPE:
                                self.in_settings = False
                                self.in_menu = True
                        elif event.type == pygame.KEYUP:
                            key_hold_time = 0

                    elif self.in_pause_settings:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.pause_menu_settings.navigate(-1)
                            elif event.key == pygame.K_DOWN:
                                self.pause_menu_settings.navigate(1)
                            elif event.key == pygame.K_LEFT:
                                self.pause_menu_settings.adjust_gamma(-1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RIGHT:
                                self.pause_menu_settings.adjust_gamma(1)
                                key_hold_time = pygame.time.get_ticks()
                            elif event.key == pygame.K_RETURN:
                                option, value = self.pause_menu_settings.toggle_option()
                                if option == "Fullscreen":
                                    self.toggle_fullscreen(borderless=False)
                                elif option == "Borderless":
                                    self.toggle_fullscreen(borderless=True)
                                elif option == "Resolution":
                                    self.apply_resolution(value)
                                    self.settings.set_option("Fullscreen", False)  # Ensure fullscreen is off
                                elif option == "Back":
                                    self.in_pause_settings = False
                                    self.in_pause = True
                            elif event.key == pygame.K_y:
                                fullscreen_before_reset = self.settings.options[0]["value"]
                                self.main_menu_settings.reset_settings()  # Reset settings to default
                                self.pause_menu_settings.reset_settings()  # Reset pause menu settings to default
                                self.settings.set_option("Fullscreen", fullscreen_before_reset)
                            elif event.key == pygame.K_ESCAPE:
                                self.in_pause_settings = False
                                self.in_pause = True

                    elif self.in_gameplay:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.in_pause = True
                                self.audio_manager.stop_music()
                                self.audio_manager.play_music("../audio/pause_menu.ogg", loops=-1, volume=0.5)
                            elif event.key == pygame.K_f:
                                self.toggle_fullscreen()
                            elif event.key == pygame.K_u:
                                self.in_upgrade = True
                                self.level.toggle_menu()

                        if event.type == pygame.VIDEORESIZE:
                            global WIDTH, HEIGTH
                            WIDTH, HEIGTH = event.size
                            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
                            self.level.floor_surf = pygame.transform.scale(pygame.image.load('../graphics/tilemap/ground.png').convert(), (WIDTH, HEIGTH))  # Scale the background image

                    elif self.in_upgrade:
                        if event.type == pygame.KEYDOWN and (event.key == pygame.K_u or event.key == pygame.K_ESCAPE):
                            self.in_upgrade = False
                            self.level.toggle_menu()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    if pygame.time.get_ticks() - key_hold_time > 100:
                        self.main_menu_settings.adjust_gamma(-1)
                        key_hold_time = pygame.time.get_ticks()
                elif keys[pygame.K_RIGHT]:
                    if pygame.time.get_ticks() - key_hold_time > 100:
                        self.main_menu_settings.adjust_gamma(1)
                        key_hold_time = pygame.time.get_ticks()

                if self.in_menu:
                    self.main_menu.display()
                    
                elif self.in_pause:
                    self.screen.fill(WATER_COLOR)
                    self.level.visible_sprites.custom_draw(self.level.player)
                    self.level.ui.display(self.level.player)  
                    self.pause_menu.display()
                    
                elif self.in_settings:
                    self.main_menu_settings.display()
                    
                elif self.in_pause_settings:
                    self.pause_menu_settings.display()
                    
                elif self.in_gameplay:
                    self.screen.fill(WATER_COLOR)
                    self.level.run()
                    #show_fps(self.clock)  # Show FPS
                    #show_memory_usage()  # Show memory usage
                    
                    pygame.display.update()

                elif self.in_upgrade:
                    if self.level.upgrade.display():
                        self.in_upgrade = False
                        self.level.toggle_menu()

                self.clock.tick(FPS)
        finally:
            self.cleanup()

    def cleanup(self):
        if os.path.exists(CHUNKS_FOLDER):
            shutil.rmtree(CHUNKS_FOLDER)

    def toggle_fullscreen(self, borderless=False):
        if borderless:
            pygame.display.set_mode((WIDTH, HEIGTH), pygame.NOFRAME)  
            self.fullscreen = False  
        else:
            if self.fullscreen:
                pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)  
                self.fullscreen = False
            else:
                pygame.display.set_mode((WIDTH, HEIGTH), pygame.FULLSCREEN) 
                self.fullscreen = True

        
        self.level.floor_surf = pygame.transform.scale(
            pygame.image.load('../graphics/tilemap/ground.png').convert(), (WIDTH, HEIGTH)
        )
        self.level.visible_sprites.offset = pygame.math.Vector2(0, 0)  
    
    def apply_resolution(self, resolution):
        global WIDTH, HEIGTH
        WIDTH, HEIGTH = resolution
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
        self.level.floor_surf = pygame.transform.scale(pygame.image.load('../graphics/tilemap/ground.png').convert(), (WIDTH, HEIGTH))  # Scale the background image

if __name__ == '__main__':
    game = Game()
    game.run()