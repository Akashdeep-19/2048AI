import pygame as pg 
import random
import numpy as np

width = 400
height = 400
# state = np.zeros((4,4),dtype = int)
# actual_state = state.copy()
#actions = [up,right,down,left]
actions = [(0,1),(-1,0),(0,-1),(1,0)]
#score = 0
#actual_score = 0
white = (255,255,255)
blue = (20,80,150)
black = (0,0,0)
w = 80
cords = [(i//4,i%4) for i in range(16)]

def rand_num(p = 0.8,state = None):
    b = np.where(state == 0)
    b = list(zip(b[0],b[1]))
    if len(b) == 0:
        return state
    a = random.randint(0,len(b)-1)
    if(random.random() < p):
        state[b[a]] = 2
    else:
        state[b[a]] = 4
    return state

def move_cells(c,state):
    
    for i in range(4):
        if(c[0] == 0):
            s = state[i,:]
            ci = c[1]
        else:
            s = state[:,i]
            ci = c[0]
        k = 0
        for j in range(4):
            if ci == 1:
                ii = j
            else :
                ii = 4-j-1
            if s[ii] == 0:
                k += 1
            elif k != 0:
                s[ii-ci*k] = s[ii]
                s[ii] = 0  
    return state    

def combine_cells(c,state):
    score = 0
    for i in range(4):
        if(c[0] == 0):
            s = state[i,:]
            ci = c[1]
        else:
            s = state[:,i]
            ci = c[0]
        for j in range(3):
            if ci == 1:
                ii = j
            else :
                ii = 4-j-1
            if s[ii] == s[ii+ci]:
                s[ii] = s[ii]*2
                s[ii+ci] = 0
                score += s[ii]
    return (state,score)


def setup():
    state = np.zeros((4,4),dtype = int)
    state = rand_num(state = state)
    state = rand_num(state= state)
    score = 0
    return (state,score)

def update(c,state = None):
    c = actions[c]
    prev = state.copy()
    state = move_cells(c,state)
    state,score = combine_cells(c,state)
    state = move_cells(c,state)
    state = rand_num(state = state)
    if np.array_equal(prev,state):
        score = -1
        return (state,score,True)
    return (state,score,False)

# def return_to_actual():
#     state = actual_state.copy()
#     score = actual_score

def render(ai = True,keep = True,action = None,fps = 60,state = None,score = 0):
    loop = True
    if type(state) == None:
        state,total_score = setup()
    else:
        total_score = score
        
    pg.init()
    canvas = pg.display.set_mode((width,height))
    clock = pg.time.Clock()

    def disp(msg,x,y,s):
        font  = pg.font.Font('freesansbold.ttf', s)
        text = font.render(msg,True,white,black)
        text_rect = text.get_rect()
        text_rect.center = (x,y)
        canvas.blit(text,text_rect)

    while loop:
        canvas.fill((0,0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                print('quit')
                return
            if event.type == pg.KEYDOWN and not ai:
                if event.key == pg.K_UP:
                    state,score,go = update(0,state)
                    total_score += score
                if event.key == pg.K_RIGHT:
                    state,score,go = update(1,state)
                    total_score += score
                if event.key == pg.K_DOWN:
                    state,score,go = update(2,state)
                    total_score += score
                if event.key == pg.K_LEFT:
                    state,score,go = update(3,state)
                    total_score += score

        if action != None:
            state,score,go = update(action,state)
            total_score += score
            if go:
                action = None
                print('gameover')
        
        for i in cords:
            disp(str(state[i]),w+i[0]*w,w+i[1]*w,32)
        disp(str(total_score),100,20,32)
        pg.display.flip()
        if not keep:
            #pg.quit()
            return
        clock.tick(fps)


# state = np.array([[4,8,2,8],
#                 [8,2,16, 64],
#                 [ 2, 16, 32, 16],
#                 [ 8,  4 , 2 , 4]])

# state = move_cells((0,1),state)
# print(state)
# state,s = combine_cells((0,1),state)
# print(state,s)
# state = move_cells((0,1),state)
# print(state)
# state = rand_num(state = state)
# print(state)

