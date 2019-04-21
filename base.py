import pygame
from time import perf_counter,time
from random import choice, randint

# CONST
black = (10, 10, 10)
white = (100, 100, 100)
backgroundColor = (158, 158, 158)
XVERL=6
YVERL=5
JUMPFORCE=9.5
GRAVITY=0.7
# get image
birdImage = pygame.image.load('data/bird.png')
deadBird = pygame.image.load('data/deadBird.png')
spikeImage = pygame.image.load('data/spike.png')
homeScreen = pygame.image.load('data/home.png')
text1 = pygame.image.load('data/text1.png')
text2 = pygame.image.load('data/text2.png')
soloButton = pygame.image.load('data/button1.png')
dualButton = pygame.image.load('data/button2.png')
botButton = pygame.image.load('data/button3.png')
arrow = pygame.image.load('data/arrow.png')

# pygame init
pygame.init()
clock = pygame.time.Clock()
screenSize = (300, 500)
screen = pygame.display.set_mode(screenSize)
myFont = pygame.font.SysFont("AdobeFanHeitiStd-Bold", 30)
scoreFont = pygame.font.SysFont('Cooper Black', 100)
spikeSize = (20, 40)


def showSpikes(leftSpike, rightSpike):
    for spike in range(len(leftSpike)):
        if leftSpike[spike]:
            screen.blit(spikeImage, (9, spike * spikeSize[1] + 10))
        if rightSpike[spike]:
            screen.blit(pygame.transform.flip(spikeImage, True, False),
                        (screenSize[0] - spikeSize[0] - 11, spike * spikeSize[1] + 10))
    for i in range(7):
        downSpike = pygame.transform.rotate(spikeImage, -90)
        screen.blit(downSpike, (9 + i * 40, 9))
    for i in range(7):
        upSpike = pygame.transform.rotate(spikeImage, 90)
        screen.blit(upSpike, (9 + i * 40, screenSize[1] - 31))


def getTime():
    return time()


def showScore(score):
    scoreText = scoreFont.render(str(score), True, (158, 158, 158))
    coor = scoreText.get_size()
    pygame.draw.circle(screen, (130, 130, 130), (150, 250), 80)
    screen.blit(scoreText, (screenSize[0] // 2 - coor[0] // 2, screenSize[1] // 2 - coor[1] // 2 - 10))


def genSpike(score):
    spike = [0] * 12
    number = [2, 3, 3, 4, 4, 4]
    if score // 4 > 6:
        score = 24
    for i in range(len(number)):
        number[i] += score // 4
    number = choice(number)
    while sum(spike) < number:
        spike[randint(0, 11)] = 1
    return spike


def curHightScore():
    scoreFile = open('data/score.txt')
    a = scoreFile.read()
    scoreFile.close()
    return int(a)


def updateHightScore(newHightScore):
    scoreFile = open('data/score.txt', 'w')
    scoreFile.write(str(newHightScore))
    scoreFile.close()
