#-*- coding: UTF-8 -*-
from random import randint
HEIGHT = 600
WIDTH = 600
UNIT = 20
BORDER_WIDTH = 10

class MoveResult:
    def __init__(self, is_alive, worm_eated):
        self.is_alive = is_alive
        self.worm_eated = worm_eated

class SnakeGame:
    def xy_index(self, x, y):
        return x + y * self.width
        
    def restart(self):
        self.is_over = False
        self.score = 0
        self.snakebody = []
        self.space = []
        self.snakedirct = 'up'
        self.dirct_changed = False
        self.worm = ()
        self.__init_snake_body__()
        self.__first_calcu_space__()
        self.__make_worm__()
    
    def __init__(self):
        self.is_over = False
        self.score = 0
        self.width = WIDTH / UNIT
        self.height = HEIGHT / UNIT
        self.unit_num = self.width * self.height
        self.snakebody = []
        self.__init_snake_body__()
        self.space = []
        self.__first_calcu_space__()
        self.snakedirct = 'up'
        self.dirct_changed = False
        self.worm = ()
        self.__make_worm__()
        
    def __init_snake_body__(self):
        rangex = (self.width / 10 * 3 - 1, self.width / 10 * 7 - 1)
        rangey = (self.height / 10 * 3 - 1, self.height / 10 * 7 - 1)
        if rangey[1] + 1 >= self.height or  rangey[1] - 1 < 0:
            raise RuntimeError("the height is too small!",
                               "in __init_snake_bogy__")
        snakehead = (randint(rangex[0], rangex[1]),
                            randint(rangey[0], rangey[1]))
        self.snakebody.append(snakehead)
        self.snakebody.append((snakehead[0], snakehead[1] + 1))

    def __first_calcu_space__(self):
        width = self.width
        space = [x for x in range(self.unit_num)]
        for (x, y) in self.snakebody:
            space.remove(self.xy_index(x, y))
        self.space = space

    def __make_worm__(self):
        maxindex = len(self.space) - 1
        index = randint(0, maxindex)
        tindex = self.space[index]
        self.worm  = (tindex % self.width, tindex / self.width)
        self.space.remove(tindex)
        
    def set_dirct(self, dirct):
        if dirct is None:
            raise ValueError("direct is None!", "in set_dirct")
        if self.dirct_changed or self.snakedirct == dirct:
            return 
        if dirct == "up" and self.snakedirct == "down":
            return
        if dirct == "down" and self.snakedirct == "up":
            return
        if dirct == "left" and self.snakedirct == "right":
            return
        if dirct == "right" and self.snakedirct == "left":
            return
        self.snakedirct = dirct
        self.dirct_changed = True
        
    def move(self):
        dirct = self.snakedirct
        head = self.snakebody[0]
        if "up" == dirct:
            head = (head[0], head[1] - 1)
        elif "down" == dirct:
            head = (head[0], head[1] + 1)
        elif "left" == dirct:
            head = (head[0] - 1, head[1])
        elif "right" == dirct:
            head = (head[0] + 1, head[1])
        else:
            raise ValueError("invalid dirct!", "in move")
        self.head = head
        if head[0] >= self.width or head[1] >= self.height \
            or head[0] < 0 or head[1] < 0 or head in self.snakebody:
            is_alive = False
            self.is_over = True
            worm_eated = False
            return MoveResult(is_alive, worm_eated)   
        
        is_alive = True
        worm_eated = False
        if head == self.worm:
            worm_eated = True
        
        if not worm_eated:
            tail = self.snakebody.pop()
            self.space.append(self.xy_index(tail[0], tail[1]))
            self.space.remove(self.xy_index(head[0], head[1]))
            
        self.snakebody.insert(0, head)
        
        
        if worm_eated:
            self.__make_worm__()
            self.score += 1
        
        self.dirct_changed = False
        return MoveResult(is_alive, worm_eated)   


'''--------------------------------------------------------------------------'''

from Tkinter import *
import tkFont

'''
keycode:
left    :  37
up      :  38
right   :  39
down    :  40
enter   :  13
esc     :  27
q(quit) :  81
s(stop) :  83
space   :  32
'''

'''
height : 600
width  : 600
bordewidth : 10
pixel_unit  : h:20 w:20

'''



   
def canvasClear(cv, front = True, game = True, over = True):
    if front:
        for id in cv_frontid:
            cv.delete(id)
        cv_frontid[:] = []
    if game:
        for id in cv_gameid:
            cv.delete(id)
        cv_gameid[:] = []
    if over:
        for id in cv_overid:
            cv.delete(id)
        cv_overid[:] = []
      
    
def drawPoint(canvas, x, y):
    tx = BORDER_WIDTH + x * UNIT
    ty = BORDER_WIDTH + y * UNIT
    #print "tx = %d, ty = %d" %(tx, ty)
    return canvas.create_rectangle((tx, ty, tx + UNIT, ty + UNIT), fill = "white")
    
def drawTitle():
    global root
    if state != "select":
        root.title("Snake state:[%s] direct:[%s] score:[%d] isAlive:[%s]" %(state, game.snakedirct, game.score, str(result.is_alive)))
    else:
        root.title("Snake state:[select]")
    root.update()
        
    
 
def drawGameFront(cv):
    canvasClear(cv)
    hint = "type <esc> or \'q\' to quit\n\
type <enter> to confirm\n\
type <up> or <down> to select\n\
type \'s\' to stop and resume when play\n\
type <space> to accelerate when play"
    cv_frontid.append(cv.create_text((200, 480), text = hint, fill = "#888888", font = smallfont)) 
    cv_frontid.append(cv.create_text((310, 250), text = "==SNAKE==", fill = "white", font = bigfont))
    cv_frontid.append(cv.create_text((480, 440), text = "play", fill = "white", font = font))
    cv_frontid.append(cv.create_text((480, 480), text = "quit", fill = "white", font = font))
    if selected == 0:
        sx = 400
        sy = 430
    else:
        sx = 400
        sy = 470
    cv_frontid.append(cv.create_rectangle((sx, sy, sx + UNIT, sy + UNIT), fill = "white"))
    
def drawMainGame(cv, game):
    canvasClear(cv)
    worm = game.worm
    snakebody = game.snakebody
    cv_gameid.append(drawPoint(cv, worm[0], worm[1]))
    for (x, y) in snakebody:
        cv_gameid.append(drawPoint(cv, x, y))
        
def drawOver(cv, game):
    for id in cv_gameid:
        cv.itemconfigure(id, fill = "#666666")   #color : gray
    cv_overid.append(cv.create_text((310,150), text = "score:%d" %game.score, fill = "white", font = font))
    cv_overid.append(cv.create_text((310,310),  text = "game over", fill = "white", font = bigfont))
    cv_overid.append(cv.create_text((310, 450), text = "type enter to continue...", fill = "white", font = font))
    
def timerHandler():
    global state
    global game
    global root
    global result
    global isStop
    global isAccelerate
    if state == "play" or state == "stop":
        if not isStop:
            result =  game.move()
            drawMainGame(cv, game)
            drawTitle()
            root.update()
            if not result.is_alive:
                state = "over"
                drawOver(cv, game)
                drawTitle()
                root.update()
        secs = 600
        if isAccelerate:
            secs = 100
        if xMode:
            secs = 10
        root.after(secs, timerHandler) 
           

    
def keyHandler(event):
    #print "keycode:" + str(event.keycode) + " char:" + event.char + " keysym:" + event.keysym + " keysym_num:" + str(event.keysym_num)
    #print "state" + str(event.state)
    #cv.create_rectangle((10,10,30,30), fill = "white")
    keycode = event.keycode
    keysym = event.keysym
    global selected
    global state
    global isStop
    if keysym == "Escape" or keysym == "q": #esc or q 
        root.quit()
    elif state == "select":
        if keysym == "Up" or keysym == "Down": #up or down
            if selected == 0:
                selected = 1
            else:
                selected = 0
            drawGameFront(cv)
        elif keysym == "Return":  #enter
            if selected == 0:
                state = "play"
                isStop = False
                isAccelerate = False
                timerHandler()
            elif selected == 1:
                root.quit()
    elif state == "over":
        if keysym == "Return": #enter
            game.restart()
            drawTitle()
            drawGameFront(cv)
            isAccelerate = False
            xMode = False
            state = "select"
    else:
        if keysym == "s": #s
            if state == "play":
                state = "stop"
                isStop = True
                drawTitle()
            elif state == "stop":
                state = "play"
                isStop = False
                drawTitle()
        elif state == "play":
            if keysym == "Left": #left
                game.set_dirct("left")
            elif keysym == "Up": #up
                game.set_dirct("up")
            elif keysym == "Right": #right
                game.set_dirct("right")
            elif keysym == "Down": #down
                game.set_dirct("down")

def spaceHandler(event):
    global state
    global isAccelerate
    if state == "play":
        if isAccelerate:
            isAccelerate = False
        else:
            isAccelerate = True
         
def xModeHandler(event):
    global state
    global xMode
    if state == "play":
        if xMode:
            xMode = False;
        else:
            xMode = True;
        


if __name__ == "__main__":
    global game
    global result
    global root
    global cv
    global state
    global selected
    global isStop
    global isAccelerate
    global xMode

    game = SnakeGame()

    #print game.worm
    #print game.snakebody

    root = Tk()
    smallfont = tkFont.Font(family='Helvetica', size = 15, weight = "bold")
    font = tkFont.Font(family='Helvetica', size = 20, weight = "bold")
    bigfont = tkFont.Font(family='Helvetica', size = 50, weight = 'bold')
    cv = Canvas(root, bg = "black", height = 620, width = 620)
    

    state = "select" #state:select,play,stop,over
    selected = 0  #selected: 0:play 1:quit

    cv_frontid = []
    cv_gameid = []
    cv_overid = []
    
    
    cv.bind_all("<Key>", keyHandler)
    cv.bind_all("<space>", spaceHandler, True)
    cv.bind_all("x", xModeHandler, True)


    cv.pack()
            
    isAccelerate = False
    xMode = False
    isStop = True
    drawTitle()
    drawGameFront(cv)
    #drawMainGame(cv, game)

    root.mainloop()

