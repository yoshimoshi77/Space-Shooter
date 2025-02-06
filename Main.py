import pygame
from sys import exit 
import random
import time
import threading
pygame.init()
screen = pygame.display.set_mode((600,650)) 
pygame.display.set_caption("Space Shooter")
pygame.mouse.set_visible(False)
background = pygame.image.load("Assets/Space_Shooter_Background.png").convert_alpha()
pygame.display.set_icon(pygame.image.load("Assets/Spaceship_1.png").convert_alpha())
scale = 2.5
background_frame_1 = pygame.transform.scale(background,(background.get_width()*scale,background.get_height()*scale))
background_frame_2 = background_frame_1
background_frame_1_rect = background_frame_1.get_rect(topleft = (0,0))
background_frame_2_rect = background_frame_2.get_rect(bottomleft = (0,0))
bullet_speed = 2
level = 1
FPS = 60

clock = pygame.time.Clock() 
alien_death_sound = pygame.mixer.Sound("Assets\Retro_Impact_SE.wav")
player_death_sound = pygame.mixer.Sound("Assets\Hit2_8bit_SE.wav")
power_up_sound = pygame.mixer.Sound("Assets\Gaining_Health_SE.wav")
bullet_sound = pygame.mixer.Sound("Assets/Lazer_SE.wav")
bgm = pygame.mixer.Sound("Assets/Space_Shooter_BGM.wav")

bullet_sound.set_volume(0.1)
bgm.set_volume(0.3)
bgm.play()
alien_impact = pygame.mixer.Sound("Assets\Light_Impact_SE.wav")


def get_frames(sheet,rows,columns):
    frames = []
    frame_width = int(sheet.get_width()/columns)
    frame_height = int(sheet.get_height()/rows)

    for y in range(0,sheet.get_height(),frame_height):
        for x in range(0,sheet.get_width(),frame_width):
            frame = pygame.Surface((frame_width,frame_height), pygame.SRCALPHA, 32)
            frame.blit(sheet,(0,0),(x,y,frame_width,frame_height))
            frames.append(frame)


    return frames

sheet = pygame.transform.scale(pygame.image.load("Assets/Pixel Explosion.png").convert_alpha(),(200,266.66666))
alien_explosion_frames = get_frames(sheet,4,3)

sheet2 = pygame.transform.scale(pygame.image.load("Assets/Pixel Explosion.png").convert_alpha(),(300,400))
player_explosion_frames = get_frames(sheet2,4,3)

class spaceship:
    def __init__(self):
        super().__init__()
        self.alive = True
        self.image = pygame.image.load("Assets\Space_Shooter_Ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()/1.5,self.image.get_height()/1.5))
        self.flame = pygame.image.load("Assets/Space_Shooter_Ship_Flame.png").convert_alpha()
        self.flame = pygame.transform.scale(self.flame,(self.flame.get_width()/1.5,self.flame.get_height()/1.5))
        self.rect = self.image.get_rect(midbottom = (300,600))
        self.flame_rect = self.flame.get_rect(midtop = self.rect.midbottom)
        self.timer = 200
        self.hitbox_1 = pygame.Rect(self.rect.centerx - self.image.get_width()/4,self.rect.top, self.rect.centerx - self.rect.left,self.image.get_height())
        self.hitbox_2 = pygame.Rect(self.rect.left,self.rect.centery - 10  ,self.rect.width,10)
        self.hitbox_3 = pygame.Rect(self.rect.left,self.rect.centery - 10  ,self.rect.width,10)
        self.hitboxes = [self.hitbox_1,self.hitbox_2,self.hitbox_3]

        self.bullets = 1


    def draw(self,window):
        window.blit(self.image,self.rect)
        self.draw_flame(window)
    def draw_flame(self,window):
        self.flame_rect.midtop = self.rect.midbottom
        window.blit(self.flame,self.flame_rect)

    def update_position(self):
        move()

    def update_hitboxes(self):
        self.hitbox_1 = pygame.Rect(self.rect.centerx - 10 ,self.rect.y,(self.rect.centerx - 10 - self.rect.centerx - 10) * -1 ,50)
        self.hitbox_2 = pygame.Rect(self.rect.left ,self.rect.centery - 10  ,self.rect.width,10)
        self.hitbox_3 = pygame.Rect(self.rect.left + 20 ,self.rect.centery + 10 ,60,20)
        self.hitboxes = [self.hitbox_1,self.hitbox_2,self.hitbox_3]
    def update(self):
        self.update_position()
        self.fire_bullet()
        self.update_hitboxes()

    def update_fire_rate(self):
        pygame.time.set_timer(fire_bullet_timer,self.timer)



    def fire_bullet(self):
        global fire_bullet
        if fire_bullet:
            bullet_sound.play()
            bullet_amount = self.bullets

            if bullet_amount == 1:
                bullets.add(bullet(self.rect.midtop,0))
            elif bullet_amount == 2:
                bullets.add(bullet((self.rect.centerx - 12, self.rect.y),0))
                bullets.add(bullet((self.rect.centerx + 12, self.rect.y),0))
            elif bullet_amount == 3 or bullet_amount == 4:
                global bullet_speed
                bullets.add(bullet(self.rect.midtop,-1))
                bullets.add(bullet(self.rect.midtop,1))
                bullets.add(bullet(self.rect.midtop,0))
                bullet_speed = 5
            elif bullet_amount >= 5:
                bullets.add(bullet(self.rect.midtop,-2))
                bullets.add(bullet(self.rect.midtop,-1))
                bullets.add(bullet(self.rect.midtop,1))
                bullets.add(bullet(self.rect.midtop,2))
                bullets.add(bullet(self.rect.midtop,0))
                

            fire_bullet = False

class bullet(pygame.sprite.Sprite):
    def __init__(self,start_pos,angle):
        super().__init__()
        self.image = pygame.image.load("Assets\Space_Shooter_Ship_Bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()/2.5,self.image.get_height()/2.5))
        self.image = pygame.transform.rotate(self.image,angle * -10)
        self.rect = self.image.get_rect(midbottom = start_pos)
        self.angle = angle
    def move(self,bullet_speed):
        self.rect.y -= bullet_speed
        self.rect.x += self.angle
    def update(self,bullet_speed):
        self.move(bullet_speed)
        self.delete_old_bullets()
    
    def delete_old_bullets(self):
        if self.rect.bottom <= 0:
            self.kill()

class alien(pygame.sprite.Sprite):
    def __init__(self,type,coords,power_up = False):
        super().__init__()
        self.power_up = power_up
        self.type = type
        self.alien_attack = False
        self.pos = coords
        self.return_to_pos = False
        self.go_to_pos = True
        self.target = (0,0)
        if self.type == "GREEN SLIME":
            frame_1 = pygame.image.load("Assets/Space_Shooter_Green_Slime_Alien_Frame_1.png").convert_alpha()
            frame_2 = pygame.image.load("Assets/Space_Shooter_Green_Slime_Alien_Frame_2.png").convert_alpha()

            self.frames = [frame_1,frame_2]
            self.animation_index = 0
            self.animation_speed = .02
            self.image = self.frames[self.animation_index]
            
        

        elif self.type == "BLUE SLIME":
            frame_1 = pygame.image.load("Assets/Space_Shooter_Blue_Slime_Alien_Frame_1.png").convert_alpha()
            frame_2 = pygame.image.load("Assets/Space_Shooter_Blue_Slime_Alien_Frame_2.png").convert_alpha()

            self.frames = [frame_1,frame_2]
            self.animation_index = 0
            self.animation_speed = .02
            self.image = self.frames[self.animation_index]
            

        elif self.type == "UFO":
            frame_1 = pygame.image.load("Assets/Space_Shooter_UFO_Alien_Frame_1.png").convert_alpha()
            frame_2 = pygame.image.load("Assets/Space_Shooter_UFO_Alien_Frame_2.png").convert_alpha()

            self.frames = [frame_1,frame_2]
            self.animation_index = 0
            self.animation_speed = .02
            self.image = self.frames[self.animation_index]

        
        scale = 1.5
        index = 0
        for image in self.frames:
            image = pygame.transform.scale(image,(image.get_width()/scale,image.get_height()/scale))
            self.frames[index] = image
            index += 1

        if self.type == "UFO":
            self.health = 25
        elif self.type == "BLUE SLIME":
            self.health = 10
        else:
            self.health = 5

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midtop = (coords[0] - 600,coords[1]))

        self.direction = "R"
    def animate(self):
        if self.go_to_pos == False:
            if self.animation_index == 0:
                self.animation_index = 1
            else:
                self.animation_index = 0
            self.image = self.frames[self.animation_index]
            if self.direction == "L":
                self.direction = "R"
            else:
                self.direction = "L"

    
    def move(self):
        if self.alien_attack == False and self.return_to_pos == False and self.go_to_pos == False:
            if self.type != "UFO":
                if self.direction == "L":
                    self.rect.x = self.rect.x - 1
                else:
                    self.rect.x = self.rect.x + 1
            else:
                if self.direction == "L":
                    self.rect.y += 1
                else:
                    self.rect.y -= 1
                    

    def ufo_attack(self):
        if self.type == "UFO":
            if self.alien_attack:
                if not self.target[0] - 4 <= self.rect.centerx <=  self.target[0] + 4:
                    if self.target[0] < self.rect.centerx:
                        self.rect.x -= 4
                    elif self.target[0] > self.rect.centerx:
                        self.rect.x += 4

                if not self.target[1] - 4 <= self.rect.centery <=  self.target[1] + 4:
                    if self.target[1] < self.rect.centery:
                        self.rect.y -= 4
                    elif self.target[1] > self.rect.centery:
                        self.rect.y += 4


                if self.target[0] - 4 <= self.rect.centerx <=  self.target[0] + 4 and self.target[1] - 4 <= self.rect.centery <=  self.target[1] + 4 :
                    self.alien_attack = False
                    self.return_to_pos = True

            elif self.return_to_pos:
                if not self.pos[0] - 3 <= self.rect.x <=  self.pos[0] + 3:
                    if self.pos[0] < self.rect.x:
                        self.rect.x -= 3
                    elif self.pos[0] > self.rect.x:
                        self.rect.x += 3

                if not self.pos[1] - 3 <= self.rect.y <=  self.pos[1] + 3:  
                    if self.pos[1] < self.rect.y:
                        self.rect.y -= 3
                    elif self.pos[1] > self.rect.y:
                        self.rect.y += 3

                        
                if self.pos[0] - 3 <= self.rect.x <=  self.pos[0] + 3 and self.pos[1] - 3 <= self.rect.y <=  self.pos[1] + 3:
                    self.return_to_pos = False

    def shoot_bullet(self): 
        if self.type == "GREEN SLIME":
            if random.randint(1,1000) == 1:
                alien_bullets.add(alien_bullet(self.type,self.rect.midbottom))

        elif self.type == "BLUE SLIME":
            if random.randint(1,1000) == 1:
                alien_bullets.add(alien_bullet(self.type,self.rect.midbottom))



    def update(self,animation_bool):
        if animation_bool:
            self.animate()
        self.move()
        self.shoot_bullet()
        self.kill_alien()
        self.ufo_attack()
        if self.go_to_pos:
            self.rect.x += 2
            if self.rect.midtop >= self.pos:
                self.go_to_pos = False
        

    def kill_alien(self):
        if self.health <= 0:
            if self.power_up:
                power_ups.add(power_up(self.rect.center))
            explosions.add(explosion(self.rect.center))
            alien_death_sound.play()
            self.kill()

class power_up(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load("Assets/Space_Shooter_Power_Up.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image.get_width()/5,self.image.get_height()/5))
        self.rect = self.image.get_rect(center = pos)

    def move(self,speed):
        self.rect.y += speed

    def update(self,speed):
        self.move(speed)

class alien_bullet(pygame.sprite.Sprite):

    def __init__(self,type,start_pos):
        super().__init__()
        if type == "BLUE SLIME":
            self.image = pygame.image.load("Assets/Space_Shooter_Blue_Slime_Alien_Bullet.png").convert_alpha()
        elif type == "GREEN SLIME":
            self.image = pygame.image.load("Assets/Space_Shooter_Green_Slime_Alien_Bullet.png").convert_alpha()
        

        self.image = pygame.transform.scale(self.image,(self.image.get_width()/2,self.image.get_height()/2))
        self.rect = self.image.get_rect(midtop = start_pos)

    def move_down(self,speed):
        self.rect.y += speed

    def delete_old_bullets(self):
        if self.rect.x >= 650:
            self.kill()

    def update(self,speed):
        self.move_down(speed)
        self.delete_old_bullets()

class explosion(pygame.sprite.Sprite):

    def __init__(self,coords,type = "A"):

        super().__init__()
        global alien_explosion_frames
        global player_explosion_frames
        self.frames = alien_explosion_frames

        if type == "P":
            self.frames = player_explosion_frames

        self.animation_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center = coords)
        
    def update(self):
        self.image = self.frames[int(self.animation_index)]
        self.animation_index += 0.5
        if int(self.animation_index) == 12:
            self.kill()

player = spaceship()
explosions = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
aliens = pygame.sprite.Group()  
alien_bullets = pygame.sprite.Group()
bullets = pygame.sprite.Group()

fire_bullet = False
fire_bullet_timer = pygame.USEREVENT + 1
alien_animation_timer = pygame.USEREVENT + 2

pygame.time.set_timer(fire_bullet_timer,100)
pygame.time.set_timer(alien_animation_timer,400)

def make_level(level):
    alien_count = 0
    power_up_bool = False
    power_up_aliens = [random.randint(1,30)]
    if level == 1:
        for i in range(50,550,50):
            i += 30
            for j in range(50,200,50):
                aliens.add(alien("GREEN SLIME", (i,j)))
    elif level == 2:
        x = 0
        for i in range(50,550,50):
            i += 30
            for j in range(50,200,50):
                alien_count += 1
                if alien_count in power_up_aliens:
                    power_up_bool = True
                if x % 3 != 0:
                    aliens.add(alien("GREEN SLIME", (i,j),power_up_bool))
                else:
                    aliens.add(alien("BLUE SLIME", (i,j),power_up_bool))
                power_up_bool = False
                x += 1

    elif level == 3:
        alien_count += 1
        for i in range(50,550,50):
            i += 30
            for j in range(50,200,50):
                alien_count += 1
                if alien_count in power_up_aliens:
                    alien_bool = True
                else:
                    alien_bool = False
                aliens.add(alien("BLUE SLIME", (i,j),alien_bool))


    elif level == 4:
        x = 0
        for i in range(50,550,50):
            i += 30
            for j in range(50,200,50):
                alien_count += 1
                if alien_count in power_up_aliens:
                    alien_bool = True
                else:
                    alien_bool = False
                if x % 3 != 0:
                    aliens.add(alien("BLUE SLIME", (i,j + 50),alien_bool))
                else:
                    aliens.add(alien("UFO", (i,j),alien_bool))
                
                x += 1

    elif level == 5:
        for i in range(50,550,50):
            i += 30
            for j in range(50,200,75):
                alien_count += 1
                if alien_count in power_up_aliens:
                    aliens.add(alien("UFO", (i,j),True))
                else:
                    aliens.add(alien("UFO", (i,j)))

    elif level == 6:
        time.sleep(5)
        pygame.quit()
        exit()

def manage_events():
    global fire_bullet
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            player.rect.center = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: 
            pygame.quit() 
            exit() 

        elif event.type == fire_bullet_timer:
            fire_bullet = True

        elif event.type == alien_animation_timer:
            aliens.update(True)

def update_background(rect_1,rect_2):
    rect_1.y += 1
    rect_2.y += 1

    if rect_1.top >=650:
        rect_1.bottom = rect_2.top
    elif rect_2.top >= 650:
        rect_2.bottom = rect_1.top

    if rect_1.centery > rect_2.centery:
        rect_2.bottom = rect_1.top
    else:
        rect_1.bottom = rect_2.top 

    return rect_1,rect_2

def player_bullets_and_aliens_collisions():
    for bullet in bullets:
        for alien in aliens:
            if bullet.rect.colliderect(alien.rect):
                bullet.kill()
                if alien.type == "UFO":
                    if alien.alien_attack == False:
                        alien.alien_attack = True
                        alien.target = pygame.mouse.get_pos()
                if alien.health > 1:
                    alien_impact.play()
                alien.health -= 1


def player_power_up_collisions():
    for power_up in power_ups:
        if power_up.rect.colliderect(player.hitbox_1):
            player.bullets += 1
            if player.timer - 20 > 50:
                player.timer -= 20
                player.update_fire_rate()
            power_up_sound.play()
            power_up.kill()

def player_alien_collisions():
    for alien in aliens:
        for hitbox in player.hitboxes:
            if alien.rect.colliderect(hitbox):
                explosions.add(explosion(player.rect.center))
                player.alive = False
                player_death_sound.play()
                pygame.mouse.set_visible(True)


    for bullet in alien_bullets:
        for hitbox in player.hitboxes:
            if bullet.rect.colliderect(hitbox):
                bullet.kill()
                player.alive = False
                explosions.add(explosion(player.rect.center,"P"))
                pygame.mouse.set_visible(True)

def update_level():
    global level
    if len(aliens) == 0:
        level += 1
        make_level(level)


make_level(level)

def move():
    SPEED = 5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.rect.top > 0:
        player.rect.y -= SPEED
        pygame.mouse.set_pos(player.rect.center)
    if keys[pygame.K_DOWN] and player.rect.bottom <= 650:
        player.rect.y += SPEED
        pygame.mouse.set_pos(player.rect.center)
    if keys[pygame.K_LEFT] and player.rect.left > 0:
        player.rect.x -= SPEED
        pygame.mouse.set_pos(player.rect.center)
    if keys[pygame.K_RIGHT] and player.rect.right <= 650:
        player.rect.x += SPEED
        pygame.mouse.set_pos(player.rect.center)


while True: 

    screen.fill((255,255,255))
    background_frame_1_rect,background_frame_2_rect = update_background(background_frame_1_rect,background_frame_2_rect)
    screen.blit(background_frame_1,background_frame_1_rect)
    screen.blit(background_frame_2,background_frame_2_rect)
    power_ups.draw(screen)
    power_ups.update(1)
    if player.alive:
        player.draw(screen)
        player.update()
    bullets.draw(screen)
    bullets.update(5)
    aliens.draw(screen)
    aliens.update(False)
    explosions.update()
    explosions.draw(screen)
    update_level()
    alien_bullets.draw(screen)
    alien_bullets.update(3)
    player_bullets_and_aliens_collisions()
    if player.alive:
        player_power_up_collisions()
        player_alien_collisions()
    manage_events()
    pygame.display.update()
    clock.tick(FPS)