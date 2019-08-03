import game2048 as game
import time
import random

def future_scores(state = None,score = 0,n = 1):
    a = []
    if n == 0:
        return [score]
    for i in range(4):
        if score == -1:
            a = a + future_scores(state.copy(),score,n-1)
        else:
            p_state,p_score,gameover = game.update(i,state = state.copy())
            if p_score == -1:
                a = a + future_scores(p_state.copy(),p_score,n-1)
            else:
                a = a + future_scores(p_state.copy(),p_score+score,n-1)
    return a

def stratergy(state,n):
    a = future_scores(state=state.copy(),score = 0,n=n)
    return a.index(max(a))//(4**(n-1))

state,total_score = game.setup()
start = time.time()
for i in range(1000):
    state,score,go = game.update(stratergy(state.copy(),5),state = state)
    total_score += score
    #game.render(fps = 5,state= state,score= total_score,keep=False)
    #time.sleep(0.5)
    if go:
        print(i)
        break
end = time.time()
tot_time = int(end - start)
print('time :',tot_time//60,':',tot_time%60)
print(state,total_score)

game.render(fps = 5,state= state,score= total_score)




