import pygame as pg
import os
import random
from pygame import *
from pygame.locals import *
import sys
from math import *

def write(text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    WIN.blit(text, position)

def load_image(file):
    """ loads an image, prepares it for play
    """
    file = os.path.join("data","assets","images",file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert_alpha()

def load_sound(file):
    """ because pygame can be be compiled without mixer.
    """
    if not pg.mixer:
        return None
    file = os.path.join("data","assets","sound",file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None

pg.init()
pg.display.set_caption('Is Ant Alone?')
# pg.display.set_icon(pygame.image.load('icon.png'))
WIN_WIDTH, WIN_HEIGHT = pg.display.Info().current_w, pg.display.Info().current_h
WIN = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FULLSCREEN)
clock = pg.time.Clock()

UP_MOVE_KEY = K_w
RIGHT_MOVE_KEY = K_d
DOWN_MOVE_KEY = K_s
LEFT_MOVE_KEY = K_a

FPS = 60

class Player(pg.sprite.Sprite):
    image = load_image("player_sprite.png").convert_alpha()
    speed = 5
    def __init__(self):
        pg.sprite.Sprite.__init__(self,self.containers)
        self.rect = Player.image.get_rect()
        self.rect.center = (WIN_WIDTH//2,WIN_HEIGHT//2)
        self.direction = 90

    def update(self,**kwargs):
        moveDict = kwargs["moveDict"]

class Enemy(pg.sprite.Sprite):
    speed = 4
    def __init__(self,pos,angle):
        self.image = load_image("enemy_sprite.png").convert_alpha()
        pg.sprite.Sprite.__init__(self,self.containers)
        self.rect = Player.image.get_rect()
        self.pos = pos
        self.alpha_level = 0
        self.inital_pos = self.pos
        self.angle = angle
        self.target = None

    def update(self,**kwargs):
        player_direction = kwargs["player_dir"]
        moveDict = kwargs["moveDict"]

        travelling_x = 0
        travelling_y = 0
        repulsionNudgeX = 0
        repulsionNudgeY = 0
        if self.target != None:
            hyp = sqrt((self.target[0] - self.pos[0])**2 + (self.target[1] - self.pos[1])**2)
            if hyp > 0:
                travelling_x = self.speed*(self.target[0] - self.pos[0])/hyp
                travelling_y = self.speed*(self.target[1] - self.pos[1])/hyp

            for otherEnemy in FollowingAnts:
                print(otherEnemy)
                if otherEnemy != self:
                    repulsion = 20
                    distance = sqrt((otherEnemy.pos[0] - self.pos[0])**2 + (otherEnemy.pos[1] - self.pos[1])**2)
                    if distance < repulsion:
                        repulsionNudgeX += (otherEnemy.pos[0] - self.pos[0])*repulsion/distance
                        repulsionNudgeY += (otherEnemy.pos[1] - self.pos[1])*repulsion/distance


        y_diff = self.pos[1] - (WIN_HEIGHT//2)
        x_diff = self.pos[0] - (WIN_WIDTH//2)
        angle = degrees(atan2(-y_diff,x_diff))
        distance = sqrt((y_diff**2) + (x_diff**2))
        #print(distance)
        if abs(player_direction - angle) < 45 or distance <= 50:
            self.alpha_level = 255
        elif self.alpha_level > 0:
            self.alpha_level = max(0,self.alpha_level-10)
        self.image.set_alpha(self.alpha_level)

        shift_x,shift_y = getWorldShift(moveDict)

        self.pos[0] += travelling_x + repulsionNudgeX + shift_x
        self.pos[1] += travelling_y + repulsionNudgeY + shift_y
        self.rect.center = self.pos

        if self.target == None:
            if sqrt((self.pos[0] - WIN_WIDTH//2)**2 + (self.pos[1] - WIN_HEIGHT//2)**2) < 100:
                self.target = (WIN_WIDTH//2,WIN_HEIGHT//2)
                FollowingAnts.add(self)
        else:
            if sqrt((self.pos[0] - WIN_WIDTH//2)**2 + (self.pos[1] - WIN_HEIGHT//2)**2) > 140:
                self.target = None
                FollowingAnts.remove(self)


class Line():
    def __init__(self,start_pos,end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

    def getStart(self):
        return self.start_pos

    def getEnd(self):
        return self.end_pos

    def getEnds(self):
        return (self.start_pos,self.end_pos)

    def move(self,moveDict):
        shift_x,shift_y = getWorldShift(moveDict)
        self.start_pos[0] += shift_x
        self.end_pos[0] += shift_x
        self.start_pos[1] += shift_y
        self.end_pos[1] += shift_y

def getWorldShift(moveDict):
    horiontal_lean = 0
    vertical_lean = 0
    if moveDict[UP_MOVE_KEY]:
        vertical_lean -= 1
    if moveDict[DOWN_MOVE_KEY]:
        vertical_lean += 1
    if moveDict[LEFT_MOVE_KEY]:
        horiontal_lean -= 1
    if moveDict[RIGHT_MOVE_KEY]:
        horiontal_lean += 1
        
    if vertical_lean == -1:                                  # Going up
        if horiontal_lean == -1:                             #   and left
            shift_x = sqrt((Player.speed**2)/2)
            shift_y = sqrt((Player.speed**2)/2)
        elif horiontal_lean == 1:                            #   and right
            shift_x = -sqrt((Player.speed**2)/2)
            shift_y = sqrt((Player.speed**2)/2)
        else:                                                #   only
            shift_x = 0
            shift_y = Player.speed
    elif vertical_lean == 1:                                 # Going down
        if horiontal_lean == -1:                             #   and left
            shift_x = sqrt((Player.speed**2)/2)
            shift_y = -sqrt((Player.speed**2)/2)
        elif horiontal_lean == 1:                            #   and right
            shift_x = -sqrt((Player.speed**2)/2)
            shift_y = -sqrt((Player.speed**2)/2)
        else:                                                #   only
            shift_x = 0
            shift_y = -Player.speed
    else:
        if horiontal_lean == -1:                             # Going left
            shift_x = Player.speed
            shift_y = 0
        elif horiontal_lean == 1:                            # Going right
            shift_x = -Player.speed
            shift_y = 0
        else:                                                # Not moving
            shift_x = 0
            shift_y = 0

    return shift_x,shift_y

PlayerGroup = pg.sprite.Group()
EnemyGroup = pg.sprite.Group()
FollowingAnts = pg.sprite.Group()
AllGroup = pg.sprite.RenderUpdates()

Player.containers = AllGroup,PlayerGroup
Enemy.containers = AllGroup,EnemyGroup

def main():
    running = True
    player = Player()
    Enemy([WIN_WIDTH//2,200],45)
    Enemy([WIN_WIDTH*3//4,200],135)
    moveDict = {LEFT_MOVE_KEY:False,RIGHT_MOVE_KEY:False,UP_MOVE_KEY:False,DOWN_MOVE_KEY:False}
    lineList = []
    lineList.append(Line([WIN_WIDTH//2,0],[WIN_WIDTH,WIN_HEIGHT//4]))

    while running:
        clock.tick(FPS)
        for e in pg.event.get():
            if e.type == QUIT:
                running = False
                pg.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key in moveDict.keys():
                    moveDict[e.key] = True
            if e.type == KEYUP:
                if moveDict.get(e.key,False):
                    moveDict[e.key] = False
        
        player_direction = player.direction
        WIN.fill((125,125,125))
        for line in lineList:
            line.move(moveDict)
            pg.draw.line(WIN,(255,0,0),line.getStart(),line.getEnd(),width=2)
        AllGroup.update(player_dir = player_direction,moveDict = moveDict)
        AllGroup.draw(WIN)
        pg.display.update()

if __name__ == "__main__":
    main()
    
# end of file
