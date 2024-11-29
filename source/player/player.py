import pygame
from gameplay.settings import *
from core.support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect =self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        
        self.import_player_assets()
        self.status = 'down'
        

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        
        self.obstacle_sprites = obstacle_sprites
 
    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {'up':[],'down':[],'left':[],'right':[],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        #move 
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0
            
        #attack 
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')
            
        #magic
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')
    
    def get_status(self):
        
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status + '_idle'
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):
     if direction == 'horizontal':
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0: 
                    self.hitbox.right = sprite.hitbox.left
                elif self.direction.x < 0: 
                    self.hitbox.left = sprite.hitbox.right
                
                self.rect.centerx = self.hitbox.centerx
                        
     if direction == 'vertical':
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:  
                    self.hitbox.bottom = sprite.hitbox.top
                elif self.direction.y < 0: 
                    self.hitbox.top = sprite.hitbox.bottom
                
                self.rect.centery = self.hitbox.centery
    
    def colldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    def update(self):
        self.input()
        self.colldowns()
        #self.get_status()
        self.move(self.speed)