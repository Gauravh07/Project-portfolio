from tkinter import *
from Grid import Grid
from Pixel import Pixel
import time





### complete class Snake
class Snake(Grid):
    def __init__(self, root1, obstacles, fruits):
        super().__init__(root1, 50, 30, 20)
        self.obstacles = obstacles
        self.fruits = fruits
        self.random_pixels(self.obstacles, 1)
        self.random_pixels(self.fruits - 1, 3)
        self.snake = []
        self.gameover = False
        self.pause = False
       
        self.turn = False
        for x in range(3):
            self.snake += [Pixel(self.canvas, 25, 15+x, self.nrow, self.ncol, self.scale, 5, [0,1])]
        self.snake += [Pixel(self.canvas, 25, 18, self.nrow, self.ncol, self.scale, 4, [0,1])]
    
    def is_game_over(self):
        return self.gameover

    def set_game_state(self,x):
        if x==True:
         self.gameover = True

    def is_pause(self):
        return self.pause
    
    def pause(self):
        self.pause = not self.pause

    def right(self):#moving pixel  to right
        
        head = self.snake[-1]
        if head.vector[1] == 0 and self.turn == False:
            self.turn = True
            head.right()
            self.matrix[head.i][head.j] = -1
    
    def up(self):#moving pixel  to up
        head = self.snake[-1]
        if head.vector[0] == 0 and self.turn == False:
            self.turn = True
            head.up()
            self.matrix[head.i][head.j] = -2

    
    def left(self):#moving pixel to left
        head = self.snake[-1]
        if head.vector[1] == 0 and self.turn == False:
            self.turn = True
            head.left()
            self.matrix[head.i][head.j] = -3
    
    

    def down(self):#moving pixel to  down
        head = self.snake[-1]
        if head.vector[0] == 0 and self.turn == False:
            self.turn = True
            head.down()
            self.matrix[head.i][head.j] = -4
        
    def next(self):
        for x in reversed(self.snake):
            new_i, new_j = x.i, x.j
            matrix_value = self.matrix[new_i][new_j]

            if matrix_value == -1:  # if it is a right turn
                x.vector = [0, 1]
            elif matrix_value == -2:  # if it is an up turn
                x.vector = [-1, 0]
            elif matrix_value == -3:  # if it is a left turn
                x.vector = [0, -1]
            elif matrix_value == -4:  # if it is a down turn
                x.vector = [1, 0]
            if x == self.snake[0]:
                self.matrix[new_i][new_j] = 0
            x.next()
            self.turn = False
        head = self.snake[-1]
        if self.matrix[head.i][head.j] == 3:   # Checks to see if eating a fruit
            tail = self.snake[0]
            dir = tail.vector
            # Attaching new pixel to end of snake
            self.snake = [Pixel(self.canvas, tail.i - dir[0], tail.j - dir[1], self.nrow, self.ncol, self.scale, 5, dir)] + self.snake
            self.delij(head.i, head.j)   # Deletes fruit pixel
            self.fruits -= 1
            
        if self.matrix[head.i][head.j] == 1:   # Checks to see if hits an obstacle
            text=self.canvas.create_text((self.ncol*self.scale)/2,(self.nrow*self.scale)/2,text='GAME OVER',font=('Papyrus',35),fill='red')
            print(text)
            self.set_game_state(True)  
        
        for x in range(len(self.snake)-1):   # this checks if the snakes hits itslef
            if self.snake[x].i == self.snake[-1].i and self.snake[x].j == self.snake[-1].j:
                text=self.canvas.create_text((self.ncol*self.scale)/2,(self.nrow*self.scale)/2,text='GAME OVER',font=('Papyrus',35),fill='red')
                print(text)
                self.set_game_state(True)   
        if self.fruits == 0:   # Checking if any fruits remaining in the grid
            text=self.canvas.create_text((self.ncol*self.scale)/2,(self.nrow*self.scale)/2,text='YOU WON',font=('Papyrus',35),fill='green')
            print(text)
            self.set_game_state(True)   






#########################################################
############# Main code #################################
#########################################################
    

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        python = Snake(root,20,20) #20 obstacles, and 20 fruits
        #python = Snake(root,5,5,25,25,30) # 5 obstacles/fruits, 25 row, 25 column, 30 scale
        
        
        ####### Tkinter binding mouse actions
        root.bind("<Right>",lambda e:python.right())
        root.bind("<Left>",lambda e:python.left())
        root.bind("<Up>",lambda e:python.up())
        root.bind("<Down>",lambda e:python.down())
        root.bind("<p>",lambda e:python.pause())
       
        while True:
            if not python.is_pause(): python.next()
            root.update()
            time.sleep(0.15)  # wait few second (simulation)
            if python.is_game_over(): break
            
        
        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

