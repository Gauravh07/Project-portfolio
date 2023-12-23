from tkinter import *
from Grid import Grid
from Tetrominoes import Tetrominoes
import numpy as np
import time

        
### complete class Tetris
class Tetris(Grid):
    def __init__(self, root, nrow, ncol, scale):
        super().__init__(root, nrow, ncol, scale)
        self.current = None
        self.game_over = False
        self.paused = False

    def is_overlapping(self, ii, jj):#checks for overlap
        tetroArray = self.current.pattern[self.current.current][2, :]
        for x in range(len(tetroArray)):
            if tetroArray[x] != 0 and self.matrix[ii][jj+x] != 0:
                return True
        return False

    def next(self):
        if self.current is None:
            self.current = Tetrominoes.random_select(self.canvas, self.nrow, self.ncol, self.scale)
            self.current.activate()

        self.current.down()
        x = self.current.i + 1
        y = self.current.j

        if x >= self.nrow or self.is_overlapping(x, y):
            # Block is in place
            pattern = self.current.pattern[self.current.current]
            self.current.delete()
            for x in pattern:
                self.addij(x[0], x[1])

            self.current = None

            
            self.flush_rows()

        
            if any(self.matrix[i][:3] != 0 for i in range(3)):
                self.game_over = True
                self.current = None

            # Check if any rows can be flushed
            self.flush_rows()

            

    def up(self):
        if self.current is not None:
            self.current.rotate()

    def down(self):
        while not self.game_over and not self.paused and self.current is not None:
            self.next()

    def left(self):
        if self.current is not None:
            y = self.current.j - 1
            if y >= 0 and not self.is_overlapping(self.current.i, y):
                self.current.left()

    def right(self):
        if self.current is not None:
            y = self.current.j + 1
            if y< self.ncol - self.current + 1 and not self.is_overlapping(self.current.i, y):
                self.current.right()
    def is_game_over(self):
         return self.game_over

    def is_pause(self):
        return self.paused

    def pause(self):
        self.paused = not self.paused


#########################################################
############# Main code #################################
#########################################################
    

    
def main():
    ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        game=Tetris(root,36,12,25) 
        
        ####### Tkinter binding mouse actions
        root.bind("<Up>",lambda e:game.up())
        root.bind("<Left>",lambda e:game.left())
        root.bind("<Right>",lambda e:game.right())
        root.bind("<Down>",lambda e:game.down())
        root.bind("<p>",lambda e:game.pause())        

        while True:
            if not game.is_pause(): game.next()
            root.update()   # update the graphic
            time.sleep(0.25)  # wait few second (simulation)
            if game.is_game_over(): break
        
        root.mainloop() # wait until the window is closed


        

if __name__=="__main__":
    main()

