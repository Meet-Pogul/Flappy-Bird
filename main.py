import random  # for generating random numbers
import pygame
from pygame.locals import *  # Basic pygame imports

FPS = 30
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
FPSCLOCK = pygame.time.Clock()
GROUNDY = int(SCREENHEIGHT * 0.8)
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = r'gallery\sprites\bird.png'
BACKGROUND = r'gallery\sprites\background.png'
PIPE = r'gallery\sprites\pipe.png'


def getRandomPipe():
    """Generate position of two pipes (top and bottom)"""
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT -
                                          GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 200
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    for pipe in upperPipes:
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True


def welcome():
    """Shows Welcome Screen"""
    playerx = (SCREENWIDTH - GAME_SPRITES['player'].get_width())//5
    playery = (SCREENHEIGHT - GAME_SPRITES['player'].get_height())//2
    messagex = (SCREENWIDTH - GAME_SPRITES['message'].get_width())//2
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user click cross button or press esc
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()

            # start game if user press space or up
            elif (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.key == K_RETURN)) or event.type == pygame.MOUSEBUTTONDOWN:
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'],
                            (int(playerx), int(playery)))
                SCREEN.blit(GAME_SPRITES['message'],
                            (int(messagex), int(messagey)))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    SCORE = 0
    playerx = (SCREENWIDTH - GAME_SPRITES['player'].get_width())//5
    playery = (SCREENHEIGHT - GAME_SPRITES['player'].get_height())//2
    basex = 0

    # Get 2 pair of pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe2[0]['x'] += int(SCREENWIDTH/2)
    newPipe2[1]['x'] += int(SCREENWIDTH/2)

    upperPipes = [
        newPipe1[0],
        newPipe2[0]
    ]

    lowerPipes = [
        newPipe1[1],
        newPipe2[1]
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerAccVelY = 1

    playerFlapVel = -8  # velocity wile flapping
    playerFapped = True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()

            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or event.type == pygame.MOUSEBUTTONDOWN:
                if playery > 0:
                    playerVelY = playerFlapVel
                    playerFapped = True
                    GAME_SOUNDS['wing'].play()

        chrashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        # player chrash
        if chrashTest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                SCORE += 1
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFapped:
            playerVelY += playerAccVelY

        if playerFapped:
            playerFapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery += min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add new pipe when a first pipe is about go go
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if pipe is going out of the screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (int(
                upperPipe['x']), int(upperPipe['y'])))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (int(
                lowerPipe['x']), int(lowerPipe['y'])))

        SCREEN.blit(GAME_SPRITES['player'], (int(playerx), int(playery)))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))

        myDigits = [int(x) for x in list(str(SCORE))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],
                        (int(Xoffset), int(SCREENHEIGHT * 0.12)))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def main():
    # This is main function where from where game start
    pygame.init()  # initialize pygame's modules
    pygame.display.set_caption('Flappy Bird by Meet Pogul')

    # Variables
    GAME_SPRITES['numbers'] = (
        pygame.image.load(r'gallery\sprites\0.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\1.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\2.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\3.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\4.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\5.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\6.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\7.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\8.png').convert_alpha(),
        pygame.image.load(r'gallery\sprites\9.png').convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.image.load(
        r'gallery\sprites\message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load(
        r'gallery\sprites\base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    GAME_SOUNDS['die'] = pygame.mixer.Sound(r'gallery\audio\die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound(r'gallery\audio\hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound(r'gallery\audio\point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound(r'gallery\audio\swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(r'gallery\audio\wing.wav')

    while True:
        welcome()
        mainGame()


if __name__ == "__main__":
    main()
