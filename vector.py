import pygame 
import math
from sys import exit

width = 1200
height = 500

screen = pygame.display.set_mode((width,height))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


class ball(object):
    def __init__(self,x,y,radius,color):
        self.x = x 
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self,window):
        pygame.draw.circle(window,(0,0,0),(self.x,self.y),self.radius)
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius - 1)

    def ball_path(startx, starty, ower,angle,time):
        pass


def redraw_window():
    screen.fill((64,64,64)) 
    pygame.draw.line(screen,(0,0,0),line[0],line[1])
    golfball.draw(screen)
    pygame.display.update()

golfball = ball(300,494,5,(255,255,255))
x = y = time = power = angle = 0
shoot = False
run = True
while run:
    pos = pygame.mouse.get_pos()
    line = [(golfball.x,golfball.y),pos]
    redraw_window()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                shoot = True
                x = golfball.x
                y = golfball.y
                time = 0
                power = math.sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2)
                angle = 5
pygame.quit()