import pygame
import random

pygame.init()
clock = pygame.time.Clock()

x,y,m = 960,660,30
screen = pygame.display.set_mode([x,y])
running = True

pawn = ["img/Chess_plt60.png","img/Chess_pdt60.png"]
knight = ["img/Chess_nlt60.png","img/Chess_ndt60.png"]
bishop = ["img/Chess_blt60.png","img/Chess_bdt60.png"]
rook = ["img/Chess_rlt60.png","img/Chess_rdt60.png"]
queen = ["img/Chess_qlt60.png","img/Chess_qdt60.png"]
king = ["img/Chess_klt60.png","img/Chess_kdt60.png"]
#image = pygame.transform.scale(pygame.image.load("Chess_kdt60.png"),(m,m))

def initPieces():
    global m
    global pawn,knight,bishop,rook,queen,king
    p = []
    for i in range(2):
        p.append(pygame.transform.scale(pygame.image.load(pawn[i]),(m,m)))
        p.append(pygame.transform.scale(pygame.image.load(knight[i]),(m,m)))
        p.append(pygame.transform.scale(pygame.image.load(bishop[i]),(m,m)))
        p.append(pygame.transform.scale(pygame.image.load(rook[i]),(m,m)))
        p.append(pygame.transform.scale(pygame.image.load(queen[i]),(m,m)))
        p.append(pygame.transform.scale(pygame.image.load(king[i]),(m,m)))
    return p

def createBoard(p):
    global x,y,m
    b = []
    for i in range(int(x/m)):
        t = []
        for j in range(int(y/m)):
            t.append(1)
        b.append(t)
    b = generateLevel(b,p)
    return b

def generateLevel(b,p):
    global x,y,m
    c = [int(y/m)-2,1,int(y/m)-1,0]
    for i in range(2):
        it,v = 0,2+(i*6)
        while it < 8:
            r = random.randint(0,int(x/m)-1)
            #print(r,int(y/m)-2,len(b),len(b[0]))
            if b[r][c[i]] == 1:
                b[r][c[i]] = v
                it += 1
        v += 1
        it = 0
        while it < 8:
            r = random.randint(0,int(x/m)-1)
            if b[r][c[i+2]] == 1:
                b[r][c[i+2]] = v
                it += 1
                if it % 2 == 0 or it > 6:
                    v += 1
    for i in range(int(x/m)):
        for j in range(int(y/m)):
            r = random.randint(0,2)
            if b[i][j] == 1 and r == 0:
                b[i][j] = 0
    print(b)
    return b

def updateBoard(b,p):
    global x,y,m
    global screen
    global image
    screen.fill((49,46,43))
    for i in range(int(x/m)):
        for j in range(int(y/m)):
            if b[i][j] > 0:
                if i % 2 + j % 2 == 1:
                    color = (118,150,86)
                else:
                    color = (238,238,210)
                pygame.draw.rect(screen,color,(i*m,j*m,m,m))
                if b[i][j] > 1:
                    screen.blit(p[b[i][j]-2],(i*m,j*m))
    #screen.blit(image,(0,0))

def main():
    global clock
    global x,y
    global running
    pieces = initPieces()
    board = createBoard(pieces)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        updateBoard(board,pieces)
        pygame.display.update()
        clock.tick(100)
        
    pygame.quit()

main()
