from tkinter import *
from Grid import Grid
from Tetrominoes import Tetrominoes
import numpy as np
import time

        

class Tetris(Grid):

    def __init__(self,root,nrow=30,ncol=12,scale=20):
        super().__init__(root,nrow,ncol,scale)
        self.block=None
        self.__game_over=False
        self.__pause=False


    def next(self):
        if self.block is None: # or not self.block.is_active():
             self.block=Tetrominoes.random_select(self.canvas,self.nrow,self.ncol,self.scale)
             self.block.activate()
        self.block.down()

        i=self.block.i
        j=self.block.j
        h=self.block.h
        w=self.block.w

        done=False
        if i+h>=self.nrow: #reach the bottom
            #self.block.deactivate()
            done=True
        elif self.is_overlapping(i+1,j): # reach top of other block
            #self.block.deactivate()
            done=True
           
        #if not self.block.is_active():  # done block is not active anymore
        if done:
            pattern=self.block.get_pattern()
            self.block.delete()         #delete the block
            for iloc in range(h):       
                for jloc in range(w):
                    self.addij(i+iloc,j+jloc,pattern[iloc,jloc]) #add pattern of block into the grid
               
            for k in range(self.nrow):   
                if not (0 in self.matrix[k,:]): # test all filling rows
                    self.flush_row(k)         # flush

            if np.sum(self.matrix[0:3,:]!=0): # game over
                self.canvas.create_text(self.scale*self.ncol//2,self.scale*self.nrow//2,text="GAME OVER",fill="red",font=("Papyrus",25))
                self.__game_over=True

            self.block=None
        
  
    def up(self):
        if self.block: #.is_active():
            self.block.rotate()

    def left(self):
        if self.block: #.is_active():
            if self.block.j-1>=0 and not self.is_overlapping(self.block.i,self.block.j-1):
                self.block.left()

    def right(self):
        if self.block: #.is_active():
            if self.block.j+self.block.w<self.ncol and not self.is_overlapping(self.block.i,self.block.j+1):
                self.block.right()

    def down(self):
        while self.block: #.is_active():
            self.next()


    def is_overlapping(self,i,j):
        pattern=self.block.get_pattern()
        overlap=self.matrix[i:i+self.block.h,j:j+self.block.w]+pattern
        for i in range(self.block.h):
            for j in range(self.block.w):
                if pattern[i,j]!=0 and overlap[i,j]!=pattern[i,j]: # motif
                    return True
        return False


    def pause(self):
        print("Pause")
        self.__pause=not self.__pause

    def is_pause(self):
        return self.__pause

    def is_game_over(self):
        return self.__game_over




















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

