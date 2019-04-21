import pygame
from bird import *
from base import *
from NN import *
mode = 'home'
state = 'ready'
choice = 1
players = []
cTime=getTime()
lTime=getTime()
leftSpike, rightSpike = [0] * 12, genSpike(0)
readyVerl = 0.8
score = 0
DONE = False
gen=getResult(113)[0]
spikeList=getTrainSet()
# spikeList=[]
# for i in range(30):
#     spikeList.append(genSpike(i))
tick=0
while not DONE:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            DONE = True
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                mode='home'
                state='ready'
    if mode == 'home':
        screen.blit(homeScreen, (0, 0))
        screen.blit(text1, (50, 90))
        pygame.draw.rect(screen, backgroundColor, (55, 130, 200, 50))
        screen.blit(text2, (50, 130))
        pygame.draw.rect(screen, backgroundColor, (55, 160, 200, 50))
        screen.blit(soloButton, (110, 250))
        screen.blit(dualButton, (110, 320))
        screen.blit(botButton, (110, 390))
        if choice == 1:
            posite = (70, 260)
        elif choice == 2:
            posite = (70, 330)
        else:
            posite = (70, 400)
        screen.blit(arrow, posite)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if choice < 3:
                        choice += 1
                    else:
                        choice = 1
                if event.key == pygame.K_UP:
                    if choice > 1:
                        choice -= 1
                    else:
                        choice = 3
                elif event.key == 13:
                    if choice == 1:
                        mode = 'solo'
                        state = 'ready'
                    elif choice == 2:
                        mode = 'dual'
                        spike=genSpike(0)
                    else:
                        mode = 'bot'
                        spike=[0]*12
    elif mode == 'solo':
        screen.blit(homeScreen, (0, 0))
        if state == 'ready':
            if len(players) == 0:
                players.append(bird(xVerl=0, yVerl=0))
            if players[0].coordinate()[1] > 260 or players[0].coordinate()[1] < 200:
                readyVerl *= -1
                players[0].y += readyVerl
            else:
                players[0].y += readyVerl
            text = myFont.render('press SPACE to play', 1, (130, 130, 130))
            screen.blit(text, (55, 350))
            screen.blit(players[0].curImage(), players[0].coordinate())
            showSpikes(leftSpike, rightSpike)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        time = getTime()
                        state = 'playing'
                        players[0].xVerl = 5
                        players[0].jump()
                        cTime = getTime()
                        lTime = getTime()
        elif state == 'playing':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        players[0].jump()
            showSpikes(leftSpike, rightSpike)
            if 9 > players[0].x - players[0].width // 2 or players[0].x + players[0].width // 2 > screenSize[0] - 11:
                score += 1
                if players[0].xVerl > 0:
                    leftSpike = genSpike(score)
                    rightSpike = [0] * 12
                else:
                    rightSpike =  genSpike(score)
                    leftSpike = [0] * 12
            showScore(score)
            players[0].move(lTime,cTime)
            screen.blit(players[0].curImage(), players[0].coordinate())
            if players[0].isCollided(leftSpike, rightSpike):
                if curHightScore()<score:
                    updateHightScore(score)
                state = 'dead'
        elif state == 'dead':
            text = myFont.render('Dead', True, white)
            screen.blit(text, (120, 100))
            text = myFont.render('Press SPACE to play again', 1, white)
            screen.blit(text, (20, 120))
            text = myFont.render('Hight score: '+str(curHightScore()), 1, white)
            screen.blit(text, (90, 350))
            showSpikes(leftSpike, rightSpike)
            showScore(score)
            screen.blit(players[0].curImage('dead'), players[0].coordinate())
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        players = []
                        score = 0
                        leftSpike, rightSpike = [0] * 12, genSpike(0)
                        state = 'ready'
    elif mode=='dual':
        screen.blit(homeScreen, (0, 0))
        if state == 'ready':
            deadList=[]
            players=[]
            players.append(bird(xVerl=0, yVerl=0))
            players.append(bird(xVerl=0, yVerl=0))
            for count in range(len(players)):
                player=players[count]
                text = myFont.render('press SPACE and UP to play', 1, (130, 130, 130))
                screen.blit(text, (15, 350))
                if count%2:
                    screen.blit(player.curImage(), player.coordinate())
                else:
                    screen.blit(pygame.transform.flip(player.image, True, False), player.coordinate())
                showSpikes(spike, spike)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        state = 'playing'
                        players[1].xVerl = 5
                        players[0].xVerl = -5
                        player.jump()
                        cTime = getTime()
                        lTime = getTime()
        elif state == 'playing':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        players[0].jump()
                    if event.key == pygame.K_UP:
                        players[1].jump()
            showSpikes(spike,spike)
            showScore(score)
            for count in range(len(players)):
                player=players[count]
                player.move(lTime, cTime)
                screen.blit(player.curImage(), player.coordinate())
                if player.xVerl > 0:
                    leftSpike = [0] * 12
                    rightSpike = spike
                else:
                    leftSpike = spike
                    rightSpike = [0] * 12
                if player.isCollided(leftSpike, rightSpike):
                    deadList.append(count)
                    if curHightScore() < score:
                        updateHightScore(score)
                    state = 'dead'
            if (9 > players[0].x - players[0].width // 2 and players[0].xVerl < 0) or (
                    players[0].x + players[0].width // 2 > screenSize[0] - 11 and players[0].xVerl > 0):
                score += 1
                tick = 1
                # spike = genSpike(score)
            if tick > 0:
                tick += 1
                if tick == 10:
                    spike = genSpike(score)
                    tick = 0
        elif state == 'dead':
            if len(deadList)==2:
                text = myFont.render('Draw', True, white)
            else:
                text = myFont.render('player'+str(1-deadList[0]+1)+'win', True, white)
            screen.blit(text, (120, 100))
            text = myFont.render('Press SPACE to play again', 1, white)
            screen.blit(text, (20, 120))
            text = myFont.render('Hight score: ' + str(curHightScore()), 1, white)
            screen.blit(text, (90, 350))
            showSpikes(spike,spike)
            showScore(score)
            screen.blit(players[deadList[0]].curImage('dead'), players[deadList[0]].coordinate())
            screen.blit(players[1-deadList[0]].curImage(), players[1-deadList[0]].coordinate())
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        players = []
                        score = 0
                        spike= genSpike(0)
                        state = 'ready'
    elif mode=='bot':
        screen.blit(homeScreen, (0, 0))
        if state == 'ready':
            deadList = []
            players = []
            players.append(bird(xVerl=0, yVerl=0))
            players.append(bird(xVerl=0, yVerl=0))
            for count in range(len(players)):
                player = players[count]
                text = myFont.render('press SPACE to play', 1, (130, 130, 130))
                screen.blit(text, (55, 350))
                if count % 2:
                    screen.blit(player.curImage(), player.coordinate())
                else:
                    screen.blit(pygame.transform.flip(player.image, True, False), player.coordinate())
                showSpikes(spike, spike)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        state = 'playing'
                        players[1].xVerl = 5
                        players[0].xVerl = -5
                        player.jump()
                        cTime = getTime()
                        lTime = getTime()
        elif state == 'playing':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        players[1].jump()
            if players[0].xVerl > 0:
                distance = players[0].x
            else:
                distance = 300 - players[0].x
            if neuralNet(normalize((distance, players[0].y, players[0].yVerl, getSpikeHight(players[0].y, spikeList[score]))), gen):
                players[0].jump()
            showSpikes(spike, spike)
            showScore(score)
            for count in range(len(players)):
                player = players[count]
                player.move(lTime, cTime)
                screen.blit(player.curImage(), player.coordinate())
                if player.xVerl>0:
                    leftSpike=[0]*12
                    rightSpike=spike
                else:
                    leftSpike = spike
                    rightSpike =  [0] * 12
                if player.isCollided(leftSpike, rightSpike):
                    #((player.x-10<5 and player.xVerl<0) or (490-player.x<5 and player.xVerl>0)):
                    deadList.append(count)
                    if curHightScore() < score:
                        updateHightScore(score)
                    state = 'dead'
            if (9 > players[0].x - players[0].width // 2 and players[0].xVerl < 0) or (
                    players[0].x + players[0].width // 2 > screenSize[0] - 11 and players[0].xVerl > 0):
                score += 1
                tick=1
                # spike = genSpike(score)
            if tick>0:
                tick+=1
                if tick==10:
                    spike=spikeList[score]
                    tick=0
        elif state == 'dead':
            if len(deadList) == 2:
                text = myFont.render('Draw', True, white)
            else:
                if deadList[0]==0:
                    text = myFont.render('You win', True, white)
                else:
                    text = myFont.render('You lose', True, white)
            screen.blit(text, (120, 100))
            text = myFont.render('Press SPACE to play again', 1, white)
            screen.blit(text, (20, 120))
            text = myFont.render('Hight score: ' + str(curHightScore()), 1, white)
            screen.blit(text, (90, 350))
            showSpikes(spike,spike)
            showScore(score)
            screen.blit(players[deadList[0]].curImage('dead'), players[deadList[0]].coordinate())
            screen.blit(players[1 - deadList[0]].curImage(), players[1 - deadList[0]].coordinate())
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        players = []
                        score = 0
                        # spike = genSpike(0)
                        spike=[0]*12
                        state = 'ready'
    lTime = cTime
    cTime = getTime()
    pygame.display.flip()
    clock.tick(100)