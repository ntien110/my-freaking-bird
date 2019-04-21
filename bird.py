import pygame
from base import *
from time import perf_counter


class bird:
    width = 30
    height = 30
    gravity = GRAVITY
    image = birdImage

    def __init__(self, x=screenSize[0] // 2, y=screenSize[1] // 2, xVerl=XVERL, yVerl=YVERL):
        self.x = x
        self.y = y
        self.xVerl = xVerl
        self.yVerl = yVerl
        self.tale = []

    def coordinate(self):
        return [self.x - self.width // 2, self.y - self.height // 2]

    def rect(self):
        coor = self.coordinate()
        if self.xVerl > 0:
            coor[0] += 1
        else:
            coor[0] += 5 + 1
        coor[1] += 1
        return pygame.Rect(coor + [self.width - 2, self.height - 2])

    def move(self, lastTime, curTime):
        delta = curTime - lastTime
        delta *= 35
        if (9 > self.x - self.width // 2 and  self.xVerl<0 ) or (self.x + self.width // 2 > screenSize[0] - 11 and self.xVerl>0):
            self.xVerl *= -1
            if self.xVerl >= 0:
                self.x += 1
            else:
                self.x -= 1
        self.x += self.xVerl * delta
        self.yVerl += self.gravity * delta
        self.y += self.yVerl * delta

    def jump(self):
        self.yVerl = -JUMPFORCE

    def isCollided(self, leftSpike, rightSpike):
        if self.y + self.height // 2 > screenSize[1] - 27 or self.y - self.height // 2 < 25:
            return True
        for i in range(len(leftSpike)):
            rect = self.rect()
            if self.xVerl < 0 and leftSpike[i] and (rect.collidepoint(10, i * 40 + 4 + 10)
                                                    or rect.collidepoint(10, i * 40 + 35 + 10)
                                                    or rect.collidepoint(25, i * 40 + 19 + 10)
                                                    or rect.collidepoint(18, i * 40 + 12 + 10)
                                                    or rect.collidepoint(18, i * 40 + 27 + 10)):
                return True
            if self.xVerl > 0 and rightSpike[i] and (rect.collidepoint(screenSize[0] - 11, i * 40 + 4 + 10)
                                                     or rect.collidepoint(screenSize[0] - 11, i * 40 + 35 + 10)
                                                     or rect.collidepoint(screenSize[0] - 11 - 16, i * 40 + 19 + 10)
                                                     or rect.collidepoint(screenSize[0] - 11 - 8, i * 40 + 12 + 10)
                                                     or rect.collidepoint(screenSize[0] - 11 - 8, i * 40 + 27 + 10)):
                return True
        return False

    def curImage(self, state='alive'):
        if state == 'alive':
            image = self.image
        else:
            image = deadBird
        if self.xVerl < 0:
            return pygame.transform.flip(image, True, False)
        return image
