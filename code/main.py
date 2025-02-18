import pygame
import sys
import time
import shutil  
import os
import settings
from level import *

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
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(UI_FONT, 60)
        self.font_options = pygame.font.Font(UI_FONT, 40)
        self.title = "RPG ELDORIA"
        self.options = ["New Game", "Settings", "Quit Game"]
        self.selected_option = 0
        self.audio_manager = AudioManager()  

    def display(self):
        self.screen.fill(WATER_COLOR)

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

        pygame.display.flip()

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

class MainMenuSettings:
    def __init__(self, screen, settings):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, 40)
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
                
            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)
            
        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option:
            self.audio_manager.play_sound("../audio/menu/Menu9.wav", volume=2.5)
        return option, value

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
        self.font = pygame.font.Font(UI_FONT, 40)
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
                
            rendered_text = self.font.render(text, True, color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200 + idx * 50))
            self.screen.blit(rendered_text, text_rect)
            
        pygame.display.flip()

    def navigate(self, direction):
        self.settings.navigate(direction)

    def toggle_option(self):
        option, value = self.settings.toggle_option()
        if option:
            self.audio_manager.play_sound("../audio/menu/Menu9.wav", volume=2.5)
        return option, value

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

        settings.TILESIZE = config["tilesize"]
        settings.CHUNKSIZE = config["chunksize"]
        settings.VISIBLE_CHUNKS = config["visible_chunks"]
        
        self.level.wind_effect_interval = config["wind_interval"]
        self.level.wind_effect_duration = config["wind_duration"]
        self.level.max_wind_effects = config["max_wind"]

        self.level.update_wind_effects_settings()
        self.level.spawn_wind_effects()
        
    def run(self):
        try:
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
                            elif event.key == pygame.K_RETURN:
                                option, value = self.main_menu_settings.toggle_option()
                                if option == "Fullscreen":
                                    self.toggle_fullscreen(borderless=False)
                                elif option == "Borderless":
                                    self.toggle_fullscreen(borderless=True)
                                elif option == "Resolution":
                                    self.apply_resolution(value)
                                elif option == "Back":
                                    self.in_settings = False
                                    self.in_menu = True
                            elif event.key == pygame.K_ESCAPE:
                                self.in_settings = False
                                self.in_menu = True

                    elif self.in_pause_settings:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                self.pause_menu_settings.navigate(-1)
                                
                            elif event.key == pygame.K_DOWN:
                                self.pause_menu_settings.navigate(1)
                                
                            elif event.key == pygame.K_RETURN:
                                option, value = self.pause_menu_settings.toggle_option()
                                if option == "Fullscreen":
                                    self.toggle_fullscreen(borderless=False)
                                elif option == "Borderless":
                                    self.toggle_fullscreen(borderless=True)
                                elif option == "Resolution":
                                    self.apply_resolution(value)
                                elif option == "Back":
                                    self.in_pause_settings = False
                                    self.in_pause = True
                                
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

                        if event.type == pygame.VIDEORESIZE:
                            global WIDTH, HEIGTH
                            WIDTH, HEIGTH = event.size
                            self.screen = pygame.display.set_mode((WIDTH, HEIGTH), pygame.RESIZABLE)
                            self.level.floor_surf = pygame.transform.scale(pygame.image.load('../graphics/tilemap/ground.png').convert(), (WIDTH, HEIGTH))  # Scale the background image

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
                    pygame.display.update()

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