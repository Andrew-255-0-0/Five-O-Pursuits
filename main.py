import random
import pygame
from pygame import time

pygame.init()

display_width = 1024
display_height = 640

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Five-O Pursuit Testing Game')

black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
closed = False

restart = 0

class Road:
    id = 2

    def __init__(self,x,y):
        self.image = pygame.image.load("graphics/road.png")

        self.x = x
        self.y = y

        self.start_y = y

        self.setupForces()

    def loop(self):
        self.yChange()
        self.blitImage()
        self.checkForRespawn()

    def yChange(self):
        self.y += self.y_vel

    def setupForces(self):
        self.y_vel = 12

    def blitImage(self):
        game_display.blit(self.image,(self.x,self.y))

    def checkForRespawn(self):
        if self.y > self.start_y + display_height:
            self.doRespawn()

    def doRespawn(self):
        self.y = self.start_y

    def doCrash(self):
        self.doReset()

    def doReset(self):
        self.y_vel = 12
        self.image = self.image = pygame.image.load("graphics/road.png")

road_seg_1 = Road(0,-640)
road_seg_2 = Road(0,0)
road_seg_3 = Road(0,-1280)

class MainCar:
    status = 0
    id = 0

    def __init__(self):
        self.sprite = pygame.image.load("graphics/car.png")
        self.setupPositions()
        self.setupForces()

    def loop(self):
        self.posChange()
        self.blitSprite()

    # def setupHealth(self):
    #     self.health = 100

    def setupPositions(self):
        self.x_pos = display_width/2-24
        self.y_pos = display_height/2-24

    def setupForces(self):
        self.x_vel = 0.0
        self.y_vel = 0.0

    def blitSprite(self):
        game_display.blit(self.sprite, (self.x_pos,self.y_pos))

    def posChange(self):
        if self.status == 0:
            self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def doReset(self):
        self.setupForces()
        self.setupPositions()

class PoliceCar:
    id = 1
    status = 0

    def __init__(self,start_x,start_y):
        super().__init__()

        self.sprite = pygame.image.load("graphics/police car.png")

        self.start_x = start_x
        self.start_y = start_y

        self.x_pos = start_x
        self.y_pos = start_y

        self.setupForces()

    def loop(self):
        self.checkForRespawn()
        self.yChange()
        self.blitSprite()

    def setupForces(self):
        self.x_vel = 0.0
        self.y_vel = 20

    def checkForRespawn(self):
        if self.y_pos > display_height and self.status == 0:
            self.doRespawn()

    def doRespawn(self):
        self.y_pos = -128
        self.x_pos = random.randint(128+48,display_width-128-48)
        self.sprite = pygame.image.load("graphics/police car.png")

    def blitSprite(self):
        if self.sprite != None:
            game_display.blit(self.sprite, (self.x_pos,self.y_pos))

    def doCrash(self):
        self.y_vel = 0
        self.status = 1
        self.doReset()
        self.status = 0

    def yChange(self):
        self.y_pos += self.y_vel

    def doReset(self):
        self.y_pos = self.start_y
        self.x_pos = self.start_x
        self.setupForces()

main_car = MainCar()

police_car_1 = PoliceCar(random.randint(128+48,display_width-128-48),0)

def checkForCrash():
    if main_car.y_pos < police_car_1.y_pos + 115 and main_car.y_pos + 128 > police_car_1.y_pos:
        if main_car.x_pos > police_car_1.x_pos and main_car.x_pos < police_car_1.x_pos + 48 or main_car.x_pos + 48 > police_car_1.x_pos and main_car.x_pos + 48 < police_car_1.x_pos + 48:
            police_car_1.doCrash()
            road_seg_1.doCrash()
            road_seg_2.doCrash()
            road_seg_3.doCrash()
            doCrash()

def text_objects(text,font):
    text_surface = font.render(text,True,white)
    return text_surface, text_surface.get_rect()

def displayMessage(text):
    font = pygame.font.Font('freesansbold.ttf',115)
    text_surf, text_rect = text_objects(text,font)
    text_rect.center = ((display_width/2),(display_height/2))

    if text_rect is not None and text_rect is not None:
        game_display.blit(text_surf, text_rect)
        pygame.display.flip()

def doCrash():
    main_car.y_vel = 0
    main_car.status = 1
    displayMessage('You Crashed!')
    pygame.time.wait(2000)
    main_car.status = 0

    global restart
    restart = 1

def gameLoop():
    global closed

    while restart != 1:
        while not closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        main_car.x_vel -= 16
                    if event.key == pygame.K_d and main_car.x_pos < display_width - 128:
                        main_car.x_vel += 16

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        main_car.x_vel = 0
                    if event.key == pygame.K_d:
                        main_car.x_vel = 0

            if main_car.x_pos < 128:
                main_car.x_pos = 128
            if main_car.x_pos > display_width - 176:
                main_car.x_pos = display_width - 176

            checkForCrash()

            road_seg_1.loop()
            road_seg_2.loop()
            road_seg_3.loop()

            police_car_1.loop()

            main_car.loop()

            police_car_1.y_vel += 0.0125


            pygame.display.flip()
            clock.tick(30)

gameLoop()

pygame.quit()
quit()

# Ended Temporary Stuff