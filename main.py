import pygame
import random

pygame.init()
clock = pygame.time.Clock()

x,y,m = 960,660,60 #higher m = smaller board, max 120
screen = pygame.display.set_mode([x,y])
running = True
mode = 0 #0 = 1 player against ai, 1 = 2 player game, -1 = 1 player (testing)
lvl,clr,pre = 0,0,0
exp = 0 #0 = normal mode, 1 = expert mode

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

def createBoard(p,left):
    #creates the actual array matrix that holds the game board
    global x,y,m
    b = []
    for i in range(int(x/m)):
        t = []
        for j in range(int(y/m)):
            t.append(1)
        b.append(t)
    b = generateNewLevel(b,p,left)
    #b = generateRandomLevel(b,p)
    return b

def generateNewLevel(b,p,left):
    #generates new clean level with no obstacles & set piece spawn positions
    global x,y,m
    global lvl
    global exp
    nx,ny = int(x/m),int(y/m)
    h = int(nx/2)
    v = [9,7,8,10,11,8,7,9,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0,0,3,1,2,4,5,2,1,3]
    #v = [6,6,6,6,6,6,6,6,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,3,1,2,4,5,2,1,3]
    if lvl > 0:
        for i in range(16,len(v)):
            #only respawns white pieces that survived previous game
            if v[i]+2 in left:
                left.remove(v[i]+2)
            else:
                v[i] = -1
        for i in range(16,len(v)):
            #fills in leftover promoted pieces
            if len(left) == 0 and v[i] == -1:
                #white gets a free pawn every new game
                v[i] = 0
                break
            if v[i] == -1:
                v[i] = left[0]-2
                left.pop(0)
    for i in range(exp):
        v = v[:16]+v
    it,j = 0,0
    while j < ny:
        for i in range(h-4,h+4):
            b[i][j] = v[it]+2
            it += 1
        j += 1
        if j == 2+(exp*2):
            j = ny-2
    for i in range(int(x/m)):
        for j in range(int(y/m)):
            #randomly flips checkered tile into dark unmovable tile
            r = random.randint(0,3) #change this range or check below to alter randomness amount
            if b[i][j] == 1 and r == 0 and not (j == 0 and (i == h or i == h-1)):
                b[i][j] = 0
    return b

def generateRandomLevel(b,p):
    #randomly choses which tiles will be dark or checkered & where each piece starts
    global x,y,m
    h = int(x/m/2)
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
            if b[i][j] == 1 and r == 0 and not (j == 0 and (i == h or i == h-1)):
                b[i][j] = 0
    return b

def updateBoard(b,p,mv,pmv):
    #visually updates the game board after each move
    global x,y,m
    global screen
    global image
    screen.fill((49,46,43))
    h = int(x/m/2)
    for i in range(int(x/m)):
        for j in range(int(y/m)):
            if b[i][j] > 0:
                #passable tiles alternate in color to create checker pattern
                if i % 2 + j % 2 == 1:
                    color = [118,150,86]
                else:
                    color = [238,238,210]
                if j == 0 and (i == h or i == h-1):
                    #end squares for king to reach
                    for k in range(len(color)):
                        color[0] = (color[0] + 128) % 256
                pygame.draw.rect(screen,color,(i*m,j*m,m,m))
                if b[i][j] > 1:
                    #piece is drawn over tile
                    screen.blit(p[b[i][j]-2],(i*m,j*m))
    dot = [98,92,86]
    for i in range(1,len(mv)):
        #draw dots on squares that can be moved to
        pygame.draw.circle(screen,dot,(mv[i][0]*m+int(m/2),mv[i][1]*m+int(m/2)),int(m/5))
    pdot = [0,100,255]
    for i in range(len(pmv)):
        pygame.draw.circle(screen,pdot,(pmv[i][0]*m+int(m/2),pmv[i][1]*m+int(m/2)),int(m/5))
        #draw blue dots on premovable squares when applicable
        
    #screen.blit(image,(0,0))

def findAI(b,mv,a):
    #finds a random black piece to move
    global x,y,m
    nx = int(x/m)
    ny = int(y/m)
    num = a[0]
    p = []
    for i in range(nx):
        for j in range(ny):
            if b[i][j] > 7 and b[i][j] < 14:
                p.append([i,j])
    random.shuffle(p)
    for i in range(len(p)):
        t = findMoves(b,mv,1,8,p[i][0],p[i][1])
        for j in range(1,len(t)):
            #check if selected piece can move without increasing attack count
            if checkNewAttack(b,mv,t,j,num):
                return [p[i][0]*m,p[i][1]*m]
    if len(p) > 0:
        return [p[0][0]*m,p[0][1]*m]
    return [-1,-1]

def moveAI(b,mv,a):
    #randomly choses move in list
    global m
    sh = mv[1:]
    random.shuffle(sh)
    mv = [mv[0]]+sh
    if len(mv) > 2:
        num = a[0]
        for i in range(1,len(mv)):
            #check if selected move does not increase attack count
            #only applies when move count is greater than 1
            if checkNewAttack(b,mv,mv,i,num):
                return [mv[i][0]*m,mv[i][1]*m]
    return [mv[1][0]*m,mv[1][1]*m]

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
                        #separate out current and potential attack
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
            #check all moves to see which ones avoid potential attacks
            fail = False
            for k in range(len(pot)):
                if t[j] == pot[k][1]:
                    fail = True
                    break
            if not fail:
                #check if new attack appears when move is made
                swap(b,t[0],t[j])
                new = findAttacks(b,mv)
                if new[0] < num:
                    #only add move if current attacks is decreased
                    esc.append([t[0],t[j]])
                swap(b,t[0],t[j])
    if len(esc) == 0:
        return esc
    ch = random.randint(0,len(esc)-1)
    return esc[ch]

def checkNewAttack(b,mv,t,i,n):
    #check if selected move decreases attack count
    swap(b,t[0],t[i])
    new = findAttacks(b,mv)
    swap(b,t[0],t[i])
    if new[0] <= n:
        return True
    return False

def swap(b,p1,p2):
    #swaps 2 pieces on the board, used for checking attacks
    t = b[p1[0]][p1[1]]
    b[p1[0]][p1[1]] = b[p2[0]][p2[1]]
    b[p2[0]][p2[1]] = t

def randomMove(b,mv,a):
    #generate a random valid move for the ai
    mv = makeMove(findAI(b,mv,a),b,mv,[])
    cnt = 0
    while len(mv) <= 1:
        if len(mv) == 0:
            return mv
        mv = makeMove(findAI(b,mv,a),b,mv,[])
        cnt += 1
        if cnt > 20: #fail-safe break if stalemate exists
            return []
    return mv

def makeMove(pos,b,mv,pmv):
    #when selecting a piece, displays which squares can be moved to
    #when selecting an available move, makes the move with the selected piece
    global m
    global clr
    global mode
    global pre
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
            if mode != -1 and pre <= 1:
                clr = (clr+1)%2
            if pre > 1:
                pre -= 1
        elif [x,y] in pmv:
            #make premove to square, ai now makes same number of moves
            t = b[mv[0][0]][mv[0][1]]
            b[x][y] = t
            b[mv[0][0]][mv[0][1]] = 1
            if mode != 1:
                clr = (clr+1)%2
            pre = abs(mv[0][0]-x)+abs(mv[0][1]-y)
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

def findPreMoves(b,mv):
    #finds all available premoves for selected piece. currently only pawns
    x,y = mv[0][0],mv[0][1]
    lv,hv = 7,14
    pmv = []
    if b[x][y] == 2:
        i = 1
        while y-i >= 0:
            if b[x][y-i] == 1 and i > 1:
                pmv.append([x,y-i])
            else:
                if i > 1 or b[x][y-i] == 0 or checkRange(b[x][y-i],lv,hv):
                    break
            i += 1
        i = 1
        while x+i < len(b):
            if b[x+i][y] == 1 and i > 1:
                pmv.append([x+i,y])
            else:
                if i > 1 or b[x+i][y] == 0 or checkRange(b[x+i][y],lv,hv):
                    break
            i += 1
        i = 1
        while y+i < len(b[0]):
            if b[x][y+i] == 1 and i > 1:
                pmv.append([x,y+i])
            else:
                if i > 1 or b[x][y+i] == 0 or checkRange(b[x][y+i],lv,hv):
                    break
            i += 1
        i = 1
        while x-i >= 0:
            if b[x-i][y] == 1 and i > 1:
                pmv.append([x-i,y])
            else:
                if i > 1 or b[x-i][y] == 0 or checkRange(b[x-i][y],lv,hv):
                    break
            i += 1
    return pmv

def findPieces(b):
    #find and returns white pieces that are alive after game is won
    p = []
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] > 1 and b[i][j] < 8:
                p.append(b[i][j])
    return p

def checkProm(b):
    #checks if white piece has reached an end square & will promote if so
    global x,y,m
    h = int(x/m/2)
    if b[h-1][0] > 1 and b[h-1][0] < 7:
        v = b[h-1][0]
        b[h-1][0] = 1
        return v
    if b[h][0] > 1 and b[h][0] < 7:
        v = b[h][0]
        b[h][0] = 1
        return v
    return 0

def checkKing(b):
    #checks and returns the status of the white king
    #0 = alive, 1 = captured, 2 = reached the end
    global x,y,m
    h = int(x/m/2)
    if b[h-1][0] == 7 or b[h][0] == 7:
        return 2
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] == 7:
                return 0
    return 1

def main():
    global clock
    global x,y,m
    global running
    global mode,clr,lvl,pre
    pieces = initPieces()
    board = createBoard(pieces,0)
    moves = []
    caps = []
    atts = []
    left = []
    premv = []
    updateBoard(board,pieces,moves,[])
    
    while running:
        #main game loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #pressing escape key will exit the game
                    running = False
                elif event.key == pygame.K_p:
                    #switch that enables premoves
                    pre = (pre+1)%2
            elif event.type == pygame.MOUSEBUTTONUP:
                #tile is selected & action is performed when applicable
                moves = makeMove(event.pos,board,moves,premv)
                if pre > 1:
                    premv = []
                if pre == 1 and clr == 0 and len(moves) > 0:
                    premv = findPreMoves(board,moves)
                updateBoard(board,pieces,moves,premv)
                if mode == 0 and clr == 1:
                    atts = findAttacks(board,moves)
                    caps = findCaps(board,moves)
                    if atts[0] == 0 and len(caps) == 0:
                        #case1: no attacks presents & no captures possible
                        #make completely random move
                        moves = randomMove(board,moves,atts)
                    elif len(caps) > 0:
                        #case2: capture is possible regardless of attacks
                        #make completely random capture if more than one
                        ch = random.randint(0,len(caps)-1)
                        moves = caps[ch]
                    elif atts[0] > 0:
                        #case3: an attack exists & no captures possible
                        #find a way to avoid attack if possible
                        moves = avoidAttack(board,moves,atts)
                        if len(moves) == 0:
                            #no attack can be avoided, make completely random move
                            moves = randomMove(board,moves,atts)
                    if len(moves) == 0:
                        #if no move is possible, the game will reset
                        lvl += 1
                        t = findPieces(board)
                        for i in range(len(t)):
                            if t[i] != 7:
                                left.append(t[i]+1)
                            else:
                                left.append(t[i])
                        board = createBoard(board,left)
                        left = []
                        clr = 0
                        updateBoard(board,pieces,moves,[])
                        #running = False
                        break
                    moves = makeMove(moveAI(board,moves,atts),board,moves,[])
                    updateBoard(board,pieces,moves,[])
                    prom = checkProm(board)
                    if prom > 0:
                        left.append(prom+1)
                        updateBoard(board,pieces,moves,[])
                        break
                    king = checkKing(board)
                    if king > 0:
                        if king == 1:
                            #white king has been captured, the game will exit
                            running = False
                        elif king == 2:
                            #white king reached the end, the game is reset
                            lvl += 1
                            t = findPieces(board)
                            for i in range(len(t)):
                                left.append(t[i])
                            board = createBoard(board,left)
                            left = []
                            clr = 0
                            updateBoard(board,pieces,moves,[])
        pygame.display.update()
        clock.tick(100)
        
    pygame.quit()

main()
