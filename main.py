import pygame
import random

pygame.init()
clock = pygame.time.Clock()

x,y,m = 960,660,30 #higher m = smaller board
screen = pygame.display.set_mode([x,y])
running = True
mode = 1 #0 = 1 player against ai, 1 = 2 player game
clr = 0

pawn = ["img/Chess_plt60.png","img/Chess_pdt60.png"]
knight = ["img/Chess_nlt60.png","img/Chess_ndt60.png"]
bishop = ["img/Chess_blt60.png","img/Chess_bdt60.png"]
rook = ["img/Chess_rlt60.png","img/Chess_rdt60.png"]
queen = ["img/Chess_qlt60.png","img/Chess_qdt60.png"]
king = ["img/Chess_klt60.png","img/Chess_kdt60.png"]
#image = pygame.transform.scale(pygame.image.load("Chess_kdt60.png"),(m,m))

def initPieces():
    #loads black & white chess piece images into array
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
    #creates the actual array matrix that holds the game board
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
    #randomly choses which tiles will be dark or checkered & where each piece starts
    global x,y,m
    c = [int(y/m)-2,1,int(y/m)-1,0]
    for i in range(2):
        #sets up player pieces randomly for both black and white, starting with pawns
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
            #randomly flips checkered tile into dark unmovable tile
            r = random.randint(0,3) #change this range or check below to alter randomness amount
            if b[i][j] == 1 and r == 0:
                b[i][j] = 0
    #print(b)
    return b

def updateBoard(b,p,mv):
    #visually updates the game board after each move
    global x,y,m
    global screen
    global image
    screen.fill((49,46,43))
    for i in range(int(x/m)):
        for j in range(int(y/m)):
            if b[i][j] > 0:
                #passable tiles alternate in color to create checker pattern
                if i % 2 + j % 2 == 1:
                    color = (118,150,86)
                else:
                    color = (238,238,210)
                pygame.draw.rect(screen,color,(i*m,j*m,m,m))
                if b[i][j] > 1:
                    #piece is drawn over tile
                    screen.blit(p[b[i][j]-2],(i*m,j*m))
    dot = (98,92,86)
    for i in range(1,len(mv)):
        #draw dots on squares that can be moved to
        pygame.draw.circle(screen,dot,(mv[i][0]*m+int(m/2),mv[i][1]*m+int(m/2)),int(m/5))
    #screen.blit(image,(0,0))

def checkRange(v,l,h):
    #returns true if value is within range of low and high, non inclusive
    return v > l and v < h

def showMoves(pos,b,p,mv):
    #when selecting a piece, displays which squares can be moved to
    #when selecting an available move, makes the move with the selected piece
    global m
    global clr
    global mode
    lv = 7-(clr*6)
    hv = lv+7
    x = int(pos[0]/m)
    y = int(pos[1]/m)
    if len(mv) > 0 and (b[x][y] == 1 or checkRange(b[x][y],lv,hv)):
        if [x,y] in mv:
            #make move to square when available
            t = b[mv[0][0]][mv[0][1]]
            b[x][y] = t
            b[mv[0][0]][mv[0][1]] = 1
            if mode == 1:
                clr = (clr+1)%2
        mv = []
    if b[x][y] == 7+(clr*6):
        #white king
        mv = [[x,y]]
        if x > 0 and y > 0 and (b[x-1][y-1] == 1 or checkRange(b[x-1][y-1],lv,hv)):
            mv.append([x-1,y-1])
        if y > 0 and (b[x][y-1] == 1 or checkRange(b[x][y-1],lv,hv)):
            mv.append([x,y-1])
        if x < len(b)-1 and y > 0 and (b[x+1][y-1] == 1 or checkRange(b[x+1][y-1],lv,hv)):
            mv.append([x+1,y-1])
        if x < len(b)-1 and (b[x+1][y] == 1 or checkRange(b[x+1][y],lv,hv)):
            mv.append([x+1,y])
        if x < len(b)-1 and y < len(b[0])-1 and (b[x+1][y+1] == 1 or checkRange(b[x+1][y+1],lv,hv)):
            mv.append([x+1,y+1])
        if y < len(b[0])-1 and (b[x][y+1] == 1 or checkRange(b[x][y+1],lv,hv)):
            mv.append([x,y+1])
        if x > 0 and y < len(b[0])-1 and (b[x-1][y+1] == 1 or checkRange(b[x-1][y+1],lv,hv)):
            mv.append([x-1,y+1])
        if x > 0 and (b[x-1][y] == 1 or checkRange(b[x-1][y],lv,hv)):
            mv.append([x-1,y])
    if b[x][y] == 2+(clr*6):
        #white pawn
        mv = [[x,y]]
        if x > 0 and y > 0 and checkRange(b[x-1][y-1],lv,hv):
            mv.append([x-1,y-1])
        if y > 0 and b[x][y-1] == 1:
            mv.append([x,y-1])
        if x < len(b)-1 and y > 0 and checkRange(b[x+1][y-1],lv,hv):
            mv.append([x+1,y-1])
        if x < len(b)-1 and b[x+1][y] == 1:
            mv.append([x+1,y])
        if x < len(b)-1 and y < len(b[0])-1 and checkRange(b[x+1][y+1],lv,hv):
            mv.append([x+1,y+1])
        if y < len(b[0])-1 and b[x][y+1] == 1:
            mv.append([x,y+1])
        if x > 0 and y < len(b[0])-1 and checkRange(b[x-1][y+1],lv,hv):
            mv.append([x-1,y+1])
        if x > 0 and b[x-1][y] == 1:
            mv.append([x-1,y])
    if b[x][y] == 3+(clr*6):
        #white knight
        mv = [[x,y]]
        if x > 0 and y > 1 and (b[x-1][y-2] == 1 or checkRange(b[x-1][y-2],lv,hv)):
            mv.append([x-1,y-2])
        if x < len(b)-1 and y > 1 and (b[x+1][y-2] == 1 or checkRange(b[x+1][y-2],lv,hv)):
            mv.append([x+1,y-2])
        if x < len(b)-2 and y > 0 and (b[x+2][y-1] == 1 or checkRange(b[x+2][y-1],lv,hv)):
            mv.append([x+2,y-1])
        if x < len(b)-2 and y < len(b[0])-1 and (b[x+2][y+1] == 1 or checkRange(b[x+2][y+1],lv,hv)):
            mv.append([x+2,y+1])
        if x < len(b)-1 and y < len(b[0])-2 and (b[x+1][y+2] == 1 or checkRange(b[x+1][y+2],lv,hv)):
            mv.append([x+1,y+2])
        if x > 0 and y < len(b[0])-2 and (b[x-1][y+2] == 1 or checkRange(b[x-1][y+2],lv,hv)):
            mv.append([x-1,y+2])
        if x > 1 and y < len(b[0])-1 and (b[x-2][y+1] == 1 or checkRange(b[x-2][y+1],lv,hv)):
            mv.append([x-2,y+1])
        if x > 1 and y > 0 and (b[x-2][y-1] == 1 or checkRange(b[x-2][y-1],lv,hv)):
            mv.append([x-2,y-1])
    if b[x][y] == 4+(clr*6) or b[x][y] == 6+(clr*6):
        #white bishop & queen diagonal
        mv = [[x,y]]
        i,j = 1,1
        while x-i >= 0 and y-j >= 0:
            if b[x-i][y-j] == 1:
                mv.append([x-i,y-j])
            else:
                if checkRange(b[x-i][y-j],lv,hv):
                    mv.append([x-i,y-j])
                break
            i += 1
            j += 1
        i,j = 1,1
        while x+i < len(b) and y-j >= 0:
            if b[x+i][y-j] == 1:
                mv.append([x+i,y-j])
            else:
                if checkRange(b[x+i][y-j],lv,hv):
                    mv.append([x+i,y-j])
                break
            i += 1
            j += 1
        i,j = 1,1
        while x+i < len(b) and y+j < len(b[0]):
            if b[x+i][y+j] == 1:
                mv.append([x+i,y+j])
            else:
                if checkRange(b[x+i][y+j],lv,hv):
                    mv.append([x+i,y+j])
                break
            i += 1
            j += 1
        i,j = 1,1
        while x-i >= 0 and y+j < len(b[0]):
            if b[x-i][y+j] == 1:
                mv.append([x-i,y+j])
            else:
                if checkRange(b[x-i][y+j],lv,hv):
                    mv.append([x-i,y+j])
                break
            i += 1
            j += 1
    if b[x][y] == 5+(clr*6) or b[x][y] == 6+(clr*6):
        #white rook & queen up/down
        if b[x][y] == 5+(clr*6):
            mv = [[x,y]]
        i = 1
        while y-i >= 0:
            if b[x][y-i] == 1:
                mv.append([x,y-i])
            else:
                if checkRange(b[x][y-i],lv,hv):
                    mv.append([x,y-i])
                break
            i += 1
        i = 1
        while x+i < len(b):
            if b[x+i][y] == 1:
                mv.append([x+i,y])
            else:
                if checkRange(b[x+i][y],lv,hv):
                    mv.append([x+i,y])
                break
            i += 1
        i = 1
        while y+i < len(b[0]):
            if b[x][y+i] == 1:
                mv.append([x,y+i])
            else:
                if checkRange(b[x][y+i],lv,hv):
                    mv.append([x,y+i])
                break
            i += 1
        i = 1
        while x-i >= 0:
            if b[x-i][y] == 1:
                mv.append([x-i,y])
            else:
                if checkRange(b[x-i][y],lv,hv):
                    mv.append([x-i,y])
                break
            i += 1
    return mv

def main():
    global clock
    global x,y,m
    global running
    pieces = initPieces()
    board = createBoard(pieces)
    moves = []
    updateBoard(board,pieces,moves)
    
    while running:
        #main game loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                moves = showMoves(event.pos,board,pieces,moves)
                updateBoard(board,pieces,moves)
        pygame.display.update()
        clock.tick(100)
        
    pygame.quit()

main()
