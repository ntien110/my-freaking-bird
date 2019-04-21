#import pygame
from bird import *
from base import *
from random import randint,uniform
import numpy as np
from re import split

struct=[5,5,1]
spike=[]
class gene:
    def __init__(self):
        self.weight=[]
        self.bias=[]
        self.score=None
        for layer in range(len(struct)):
            self.weight.append([])
            self.bias.append([])
            for unit in range(struct[layer]):
                self.weight[layer].append([])
                if layer>0:
                    self.weight[layer][unit]=np.random.rand(1,struct[layer-1])[0]
                    for index in range(self.weight[layer][unit].size):
                        if randint(0,1):
                            self.weight[layer][unit][index]*=-1
                else:
                    self.weight[layer][unit]=np.random.rand(1,3)[0]
                    for index in range(self.weight[layer][unit].size):
                        if randint(0, 1):
                            self.weight[layer][unit][index] *= -1
                self.bias[layer].append(uniform(-1,1))

def threshold(input,weight,bias):
    arr = np.dot(input, weight.transpose())
    x=np.sum(arr) / weight.size + bias
    if x<0:
        return 0
    else:
        return 1

def linear(input,weight,bias):
    arr=np.dot(input,weight.transpose())
    return np.sum(arr)/weight.size+bias

def sigmoid(input, weight, bias):
    arr = np.dot(input, weight.transpose())
    x = np.sum(arr) / weight.size + bias
    return 1 / (1 + np.exp(-x))

def genTrainSet(size):
    file=open('trainSet.set','w')
    for i in range(size):
        file.write(str(genSpike(i))+'\n')
    file.close()

def neuralNet(input, gen):
    curValue=0
    for layer in range(len(gen.weight)-1):
        input = np.array(input)
        newInput=[]
        for unit in range(len(gen.weight[layer])):
            newInput.append(sigmoid(input,gen.weight[layer][unit],gen.bias[layer][unit]))
        input=newInput
    return threshold(input,gen.weight[len(gen.weight)-1][0],gen.bias[len(gen.weight)-1][0])

def getTrainSet():
    trainSet=[]
    file = open('trainSet.set', 'r')
    line = file.readline()
    while line:
        line = split('[\[\],\s]+', line)
        line.pop(0)
        line.pop(-1)
        for i in range(len(line)):
            line[i] = int(line[i])
        trainSet.append(line)
        line = file.readline()
    return trainSet

# def normalize(raw):
#     normalized=[0,0,0,0]
#     normalized[0]=round((raw[0]-25)/250,2)
#     normalized[1] = round((raw[1] - 25) / 450, 2)
#     if raw[2]<-JUMPFORCE:
#         normalized[2]=0
#     else:
#         normalized[2] = round(raw[2]/ JUMPFORCE, 2)
#     normalized[3] = round(raw[3] / 11, 2)
#     return normalized

def normalize(raw):
    normalized=[0,0,0]
    normalized[0]=(raw[0]-25)/250
    normalized[1] = (raw[1]-(raw[3] * 40 + 10))/400
    if raw[2]<-JUMPFORCE:
        normalized[2]=0
    else:
        normalized[2] = raw[2]/ JUMPFORCE

    return normalized

def getScore(gen):
    return gen.score

def hybrid(gen1,gen2):
    newGen=gene()
    for layer in range(len(struct)):
        for unit in range(struct[layer]):
            for weight in range(newGen.weight[layer][unit].size):
                if randint(0,1)==1:
                    newGen.weight[layer][unit][weight]=gen1.weight[layer][unit][weight]
                else:
                    newGen.weight[layer][unit][weight] = gen2.weight[layer][unit][weight]
            if randint(0, 1)==1:
                newGen.bias[layer][unit]=gen1.bias[layer][unit]
            else:
                newGen.bias[layer][unit] = gen2.bias[layer][unit]
    return newGen

def record(popu,gen):
    file=open('generations/gen_{0}.txt'.format([gen]),'w')
    for t in popu:
        file.write(str(t.weight)+str(t.bias)+str(t.score)+'\n')
    file.close()

def getResult(generation):
    file =open('generations/gen_[{0}].txt'.format(generation),'r')
    raw=file.readline()
    all=[]
    while raw:
        raw=split(r"[\s\,\[\]\(\)\array]+", raw)
        raw.pop(0)
        raw.pop(-1)
        raw.pop(-1)
        for i in range(len(raw)):
            raw[i]=float(raw[i])
        cur=gene()
        for layer in range(len(struct)):
            for unit in range(struct[layer]):
                for weight in range(cur.weight[layer][unit].size):
                    cur.weight[layer][unit][weight] = raw[0]
                    raw.pop(0)
        for layer in range(len(struct)):
            for unit in range(struct[layer]):
                cur.bias[layer][unit] = raw[0]
                raw.pop(0)
        all.append(cur)
        raw=file.readline()
    return all

def getSpikeHight(y,spikeList):
    y -= 9 + 15
    y //= 40
    cur = int(y)
    num = 0
    while spikeList[cur] != 0:
        num = abs(num) + 1
        if num % 2 == 1:
            num *= -1
        if cur+num<12 and cur+num>=0:
            cur += num
        else:
            if cur+num>=12:
                cur-=1
            else:
                cur+=1
            num=0
    temp=cur
    while temp+1<=11 and spikeList[temp+1]==0:
        temp+=1
    low=temp
    temp=cur
    while temp-1>=0 and spikeList[temp-1]==0:
        temp-=1
    hight=temp
    if cur >0 and low==cur and hight<cur:
        cur-=1
    if cur <11 and hight==cur and low>cur:
        cur+=1
    return cur

def testPlay(genList):
    pygame.init()
    result=[]
    score=0
    players =[]

    deadList = []
    for i in range(len(genList)):
        players.append(bird())
        players[i].jump()
    rightSpike = spike[score]
    leftSpike = [0] * 12
    cTime=getTime()
    lTime=getTime()
    done=False
    while not done:
        pygame.event.get()
        screen.blit(homeScreen, (0, 0))
        p=0
        while p in deadList:
            p+=1
        if (9 > players[p].x - players[p].width // 2 and players[p].xVerl<0)or(players[p].x + players[p].width // 2 > screenSize[0] - 11 and players[p].xVerl>0):
            score += 1
            if players[p].xVerl > 0:
                leftSpike = spike[score]
                rightSpike = [0] * 12
            else:
                rightSpike = spike[score]
                leftSpike = [0] * 12
        showScore(score)
        showSpikes(leftSpike, rightSpike)
        if players[0].xVerl>0:
            distance=players[0].x
        else:
            distance=300-players[0].x
        p=0
        for p in range(len(players)):
            if p not in deadList:
                player=players[p]
                hight= getSpikeHight(player.y, spike[score])

                screen.blit(pygame.transform.flip(spikeImage, True, False), (9, hight * spikeSize[1] + 10))
                screen.blit(spikeImage,(screenSize[0] - spikeSize[0] - 11, hight * spikeSize[1] + 10))

                if neuralNet(normalize((distance, player.y, player.yVerl, hight)),genList[p]):
                    player.jump()
                player.move(lTime,cTime)
                screen.blit(player.curImage(), player.coordinate())
                if player.isCollided(leftSpike, rightSpike):
                    genList[p].score=score
                    deadList.append(p)
                    if len(players)==len(deadList):
                        done=True
        lTime=cTime
        cTime = getTime()
        pygame.display.flip()
        clock.tick(60)
