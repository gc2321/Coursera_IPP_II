# simple state example for Memory

import simplegui, random

#set dictionary for numbers, state, score, count
d={}; turn =0; count =0; click_1=100; click_2=101

# define event handlers
def new_game():
    global turn, count, click_1, click_2
    turn=0; count=0; click_1=100; click_2=101
    numbers = range(8)
    numbers.extend(range(8))
    random.shuffle(numbers)
    for i in range(16):
        j = i*50
        k=(i+1)*50
        d[i]=[numbers[i], 0, [[j, 0], [j, 100], [k, 100], [k, 0]]]
    
def mouseclick(pos):
    global turn, count, click_1, click_2
      
    for i in range(16):
        if pos[0]>d[i][2][0][0] and pos[0]<d[i][2][2][0] and d[i][1]==0:
            d[i][1]=1; count +=1
            if count ==1:
                click_1 = i;
            elif count ==2:
                click_2 = i; turn +=1;
            elif count !=2:
                count = 1;  
                if d[click_1][0]!=d[click_2][0]:                   
                    d[click_1][1]=0; d[click_2][1]=0
                click_1 = i; click_2=101    
                              
def draw(canvas):
    for i in range(16):
        if d[i][1]==0:
            canvas.draw_polygon([d[i][2][0], d[i][2][1], d[i][2][2], d[i][2][3]], 3, 'Black', 'Green')
        else:
            canvas.draw_polygon([d[i][2][0], d[i][2][1], d[i][2][2], d[i][2][3]], 3, 'Black', 'Black')
            canvas.draw_text(str(d[i][0]), (d[i][2][2][0]-38, 63), 50, 'White')
    label.set_text("Turns = "+str(turn))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = "+str(turn))   

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

