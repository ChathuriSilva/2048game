import pygame
from pygame.locals import *
from constants import *
from random import *
BOARD_SIZE, TOTAL_POINTS, DEFAULT_SCORE = 4, 0, 2
pygame.init()
SURFACE = pygame.display.set_mode((400, 500), 0, 32)
tileMatrix, undoMat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],[]
def main(fromLoaded=False):
    if not fromLoaded: placeRandomTile()
    printMatrix()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit()
            if checkIfCanGo() == True:
                if event.type == KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                        rotations = getRotations(event.key)
                        undoMat.append(convertToLinearMatrix())
                        for i in range(0, rotations): rotateMatrixClockwise()
                        if canMove():
                            moveTiles()
                            mergeTiles()
                            placeRandomTile()
                        for j in range(0, (4 - rotations) % 4): rotateMatrixClockwise()
                        printMatrix()
            else: printGameOver()
            if event.type == KEYDOWN:
                global BOARD_SIZE
                if 50 < event.key and 56 > event.key: BOARD_SIZE = event.key - 48
        pygame.display.update()
def canMove():
    for i in range(0, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if tileMatrix[i][j - 1] == 0 and tileMatrix[i][j] > 0: return True
            elif (tileMatrix[i][j - 1] == tileMatrix[i][j]) and tileMatrix[i][j - 1] != 0: return True
    return False
def moveTiles():
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:
                for k in range(j, BOARD_SIZE - 1): tileMatrix[i][k] = tileMatrix[i][k + 1]
                tileMatrix[i][BOARD_SIZE - 1] = 0
def mergeTiles():
    global TOTAL_POINTS
    for i in range(0, BOARD_SIZE):
        for k in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k] * 2
                tileMatrix[i][k + 1] = 0
                TOTAL_POINTS += tileMatrix[i][k]
                moveTiles()
def placeRandomTile():
    c = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if tileMatrix[i][j] == 0: c += 1
    k = floor(random() * BOARD_SIZE * BOARD_SIZE)
    while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0: k = floor(random() * BOARD_SIZE * BOARD_SIZE)
    tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2
def floor(n):
    return int(n - (n % 1))
def printMatrix():
    SURFACE.fill(BLACK)
    global BOARD_SIZE, TOTAL_POINTS
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            pygame.draw.rect(SURFACE, getColor(tileMatrix[i][j]), (i * (400 / BOARD_SIZE), j * (400 / BOARD_SIZE) + 100, 400 / BOARD_SIZE, 400 / BOARD_SIZE))
            SURFACE.blit(pygame.font.SysFont("monospace", 40).render(str(tileMatrix[i][j]), 1, (255, 255, 255)), (i * (400 / BOARD_SIZE) + 30, j * (400 / BOARD_SIZE) + 130))
            SURFACE.blit(pygame.font.SysFont("monospace", 30).render("YourScore:" + str(TOTAL_POINTS), 1, (255, 255, 255)), (10, 20))
def checkIfCanGo():
    for i in range(0, BOARD_SIZE ** 2):
        if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0: return True
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][j] == tileMatrix[i][j + 1]: return True
            elif tileMatrix[j][i] == tileMatrix[j + 1][i]: return True
    return False
def convertToLinearMatrix():
    mat = []
    for i in range(0, BOARD_SIZE ** 2): mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])
    mat.append(TOTAL_POINTS)
    return mat
def rotateMatrixClockwise():
    for i in range(0, int(BOARD_SIZE / 2)):
        for k in range(i, BOARD_SIZE - i - 1):
            temp1, temp2 = tileMatrix[i][k], tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3, temp4 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k],tileMatrix[k][BOARD_SIZE - 1 - i]
            tileMatrix[BOARD_SIZE - 1 - k][i], tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp1, temp2
            tileMatrix[k][BOARD_SIZE - 1 - i], tileMatrix[i][k] = temp3, temp4
def printGameOver():
    global TOTAL_POINTS
    SURFACE.fill(BLACK)
    SURFACE.blit(pygame.font.SysFont("monospace", 30).render("OVER,Score: " + str(TOTAL_POINTS), 1, (255, 255, 255)), (50, 200))
def getRotations(k):
    if k == pygame.K_UP: return 0
    elif k == pygame.K_DOWN: return 2
    elif k == pygame.K_LEFT: return 1
    elif k == pygame.K_RIGHT: return 3
main()
