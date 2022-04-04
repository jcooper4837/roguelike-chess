import pygame
import random

pygame.init()
clock = pygame.time.Clock()

x,y,m = 960,660,60 #higher m = smaller board
screen = pygame.display.set_mode([x,y])
running = True
mode = 0 #0 = 1 player against ai, 1 = 2 player game, -1 = 1 player (testing)
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

def findAI(b):
    #finds a random black piece to move
    global x,y,m
    nx = int(x/m)
    ny = int(y/m)
    i = random.randint(0,nx-1)
    j = random.randint(0,ny-1)
    hi = i+nx
    hj = j+ny
    while i < hi:
        j = hj-ny
        while j < hj:
            if b[i%nx][j%ny] > 7 and b[i%nx][j%ny] < 14:
                return [i%nx*m,j%ny*m]
            j += 1
        i += 1
    return [-1,-1]

def moveAI(b,mv):
    #randomly choses move in list
    global m
    ch = random.randint(1,len(mv)-1)
    return [mv[ch][0]*m,mv[ch][1]*m]

def checkRange(v,l,h):
    #returns true if value is within range of low and high, non inclusive
    return v > l and v < h

def findCaps(b,mv):
    #find any and all captures black can make against white
    global x,y,m
    c = []
    nx = int(x/m)
    ny = int(y/m)
    for i in range(nx):
        for j in range(ny):
            if b[i][j] > 7 and b[i][j] < 14: #check only black piece moves
                t = findMoves(b,mv,1,8,i,j)
                for k in range(1,len(t)): #only add moves if they are captures
                    if b[t[k][0]][t[k][1]] > 1 and b[t[k][0]][t[k][1]] < 8:
                        c.append([[i,j],t[k]])
    return c

def findAttacks(b,mv):
    #find any and all current and potential attacks on black from white
    global x,y,m
    global clr
    clr = 0
    pot,curr = [],[]
    nx = int(x/m)
    ny = int(y/m)
    for i in range(nx):
        for j in range(ny):
            if b[i][j] > 1 and b[i][j] < 8: #check only white piece moves
                t = findMoves(b,mv,7,14,i,j)
                for k in range(1,len(t)):
                    pot.append([[i,j],t[k]])
                    if b[t[k][0]][t[k][1]] > 7 and b[t[k][0]][t[k][1]] < 14:
                        curr.append([[i,j],t[k]])
    clr = 1
    return [len(curr)]+curr+pot

def avoidAttack(b,mv,a):
    #find a way to avoid white capturing blacks pieces if possible
    num = a[0]
    curr,esc = [],[]
    for i in range(1,num+1):
        curr.append(a[i])
    pot = a[num+1:]
    for i in range(num):
        t = findMoves(b,mv,1,8,curr[i][1][0],curr[i][1][1])
        for j in range(1,len(t)):
            fail = False
            for k in range(len(pot)):
                if t[j] == pot[k][1]:
                    fail = True
                    break
            if not fail:
                swap(b,t[0],t[j])
                new = findAttacks(b,mv)
                if new[0] < num:
                    esc.append([t[0],t[j]])
                swap(b,t[0],t[j])
    if len(esc) == 0:
        return esc
    ch = random.randint(0,len(esc)-1)
    return esc[ch]

def swap(b,p1,p2):
    t = b[p1[0]][p1[1]]
    b[p1[0]][p1[1]] = b[p2[0]][p2[1]]
    b[p2[0]][p2[1]] = t

def makeMove(pos,b,mv):
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
            if mode != -1:
                clr = (clr+1)%2
        mv = []
        return mv
    return findMoves(b,mv,lv,hv,x,y)

def findMoves(b,mv,lv,hv,x,y):
    #finds all available moves for selected piece
    global m
    global clr
    global mode
    if b[x][y] == 7+(clr*6):
        #king
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
        #pawn
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
        #knight
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
        #bishop & queen diagonal
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
        #rook & queen up/down
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
    global mode,clr
    pieces = initPieces()
    board = createBoard(pieces)
    moves = []
    caps = []
    atts = []
    updateBoard(board,pieces,moves)
    
    while running:
        #main game loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                moves = makeMove(event.pos,board,moves)
                updateBoard(board,pieces,moves)
                if mode == 0 and clr == 1:
                    atts = findAttacks(board,moves)
                    caps = findCaps(board,moves)
                    if atts[0] == 0 and len(caps) == 0:
                        moves = makeMove(findAI(board),board,moves)
                        while len(moves) <= 1:
                            if len(moves) == 0:
                                running = False
                                return
                            moves = makeMove(findAI(board),board,moves)
                    elif len(caps) > 0:
                        ch = random.randint(0,len(caps)-1)
                        moves = caps[ch]
                    elif atts[0] > 0:
                        moves = avoidAttack(board,moves,atts)
                        if len(moves) == 0:
                            moves = makeMove(findAI(board),board,moves)
                            while len(moves) <= 1:
                                if len(moves) == 0:
                                    running = False
                                    return
                                moves = makeMove(findAI(board),board,moves)
                    moves = makeMove(moveAI(board,moves),board,moves)
                    updateBoard(board,pieces,moves)
        pygame.display.update()
        clock.tick(100)
        
    pygame.quit()

main()
