import pygame 
from sys import exit 
pygame.init() 
screen = pygame.display.set_mode((600,600)) 
pygame.display.set_caption("Test") 


for i in range(5): print(5); print(54)

def get_frames(sheet,rows,columns):
    frames = []
    frame_width = int(sheet.get_width()/columns)
    frame_height = int(sheet.get_height()/rows)

    for y in range(0,sheet.get_height(),frame_height):
        for x in range(0,sheet.get_width(),frame_width):
            frame = pygame.Surface((frame_width,frame_height), pygame.SRCALPHA, 32)
            frame.blit(sheet,(0,0),(x,y,frame_width,frame_height))
            frames.append(frame)

    print(len(frames))
    return frames


class explosion(pygame.sprite.Sprite):
    def __init__(self,coords,size = (300,400)):

        super().__init__()
        sheet = pygame.transform.scale(pygame.image.load("Assets/Pixel Explosion.png").convert_alpha(),(size))
        self.frames = get_frames(sheet,4,3)
        self.animation_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center = coords)
        
    def update(self):
        self.image = self.frames[int(self.animation_index)]
        self.animation_index += 0.5
        if int(self.animation_index) == 12:
            print("he")
            self.kill()
        
booms = pygame.sprite.Group()




def close_window():
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            booms.add(explosion(pygame.mouse.get_pos(),(1200,1600)))
            
clock = pygame.time.Clock()

while True: 
    screen.fill("black")
    booms.draw(screen)
    booms.update()
    close_window()
    pygame.display.update()
    clock.tick(60)


