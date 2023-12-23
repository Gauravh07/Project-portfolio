'''Team
    Name 1:Gaurav Hareesh
    Name 2: Anshuman Deodhar'''
from tkinter import *
import time
import random

class Pixel:
    """
    Class representing a pixel on the canvas.
    """

    color = ['black', 'white', 'yellow', 'red', 'blue', 'green', 'orange', 'purple', 'brown', 'cyan']

    def __init__(self, canvas, i, j, nrow, ncol, scale, c, vector=[0, 0]):
        """
        Initialize the pixel.

        Args:
            canvas: The canvas object on which the pixel is drawn.
            i (int): The row index of the pixel.
            j (int): The column index of the pixel.
            nrow (int): The number of rows in the canvas.
            ncol (int): The number of columns in the canvas.
            scale (int): The scale factor for the pixel.
            c (int): The color index of the pixel.
            vector (list): The movement vector of the pixel.

        """
        self.i = i % nrow  # modulo used for test 2 to make it not go out of the window and that it falls within nrow
        self.j = j % ncol  # modulo used for test 2 to make it not go out of the window and that it falls within ncol
        self.canvas = canvas
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.c = c
        self.vector = vector

        self.rec = canvas.create_rectangle(self.j * scale, self.i * scale, (self.j + 1) * scale,(self.i + 1) * scale, fill=self.color[self.c])

    def __str__(self):
        """
        Return the string representation of the pixel.

        Returns:
            str: The string representation of the pixel.

        """
        return "(" + str(self.i % self.nrow) + "," + str(self.j % self.ncol) + ") " + self.color[self.c]

    def next(self):
        """
        Move the pixel to the next position based on its movement vector.

        """
        self.canvas.move(self.rec, self.vector[1] * self.scale, self.vector[0] * self.scale)
        self.i += self.vector[0]
        self.j += self.vector[1]

        if self.i < 0:
            self.i = self.nrow - 1
            self.canvas.move(self.rec, 0, self.nrow * self.scale)  # Adjust vertical position
        elif self.i >= self.nrow:
            self.i = 0
            self.canvas.move(self.rec, 0, -self.nrow * self.scale)  # Adjust vertical position

        if self.j < 0:
            self.j = self.ncol - 1
            self.canvas.move(self.rec, self.ncol * self.scale, 0)  # Adjust horizontal position
        elif self.j >= self.ncol:
            self.j = 0
            self.canvas.move(self.rec, -self.ncol * self.scale, 0)  # Adjust horizontal position

    def right(self):
        """
        Change the movement vector of the pixel to move it to the right.

        """
        self.vector = [0, 1]

    def left(self):
        """
        Change the movement vector of the pixel to move it to the left.

        """
        self.vector = [0, -1]

    def up(self):
        """
        Change the movement vector of the pixel to move it up.

        """
        self.vector = [-1, 0]

    def down(self):
        """
        Change the movement vector of the pixel to move it down.

        """
        self.vector = [1, 0]

    def delete(self):
        """
        Delete the pixel from the canvas.

        """
        self.canvas.delete(self.rec)
    



                





        
          


       
    

   

    
   
    
    ### to complete        
    

















        
#################################################################
########## TESTING FUNCTION
#################################################################
def delete_all(canvas):
    canvas.delete("all")
    print("Delete All")


def test1(canvas,nrow,ncol,scale):
    print("Generate 10 points at random")
    random.seed(4) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1) 
        j=random.randint(0,ncol-1)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(pix)

def test2(canvas,nrow,ncol,scale):
    print("Generate 10 points at random (using modulo)")
    random.seed(5) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1)*34
        j=random.randint(0,ncol-1)*13
        ij=str(i)+","+str(j)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(ij,"->",pix)

        
def test3(root,canvas,nrow,ncol,scale):
    print("Move one point along a square")

    pix=Pixel(canvas,35,35,nrow,ncol,scale,3)
    pix.vector=[-1,0] # set up direction (up)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,-1] # set up new direction (left)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[1,0]   # set up new direction (down)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,1]    # set up new direction (right)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)

    #delete point
    pix.delete()


  
def test4(root,canvas,nrow,ncol,scale):
    print("Move four point along a square")

    pixs=[]
    pixs.append(Pixel(canvas,35,35,nrow,ncol,scale,3,[-1,0]))
    pixs.append(Pixel(canvas,5,35,nrow,ncol,scale,4,[0,-1]))
    pixs.append(Pixel(canvas,5,5,nrow,ncol,scale,5,[1,0]))
    pixs.append(Pixel(canvas,35,5,nrow,ncol,scale,6,[0,1]))
    
    print("Starting coords")
    for p in pixs: print(p)

    for i in range(30):
        for p in pixs:
            p.next()       # next move in the simulation     
        root.update()      # update the graphic
        time.sleep(0.05)   # wait in second (simulation)

    print("Ending coords")
    for p in pixs:
        print(p)
        p.delete()


        
def test5(root,canvas,nrow,ncol,scale):
    print("Move one point any direction -use arrow commands")

    pix=Pixel(canvas,20,20,nrow,ncol,scale,2)

    ### binding used by test5
    root.bind("<Right>",lambda e:pix.right())
    root.bind("<Left>",lambda e:pix.left())
    root.bind("<Up>",lambda e:pix.up())
    root.bind("<Down>",lambda e:pix.down())

    ### simulation
    while True:
        pix.next()
        root.update()     # update the graphic
        time.sleep(0.05)  # wait in second (simulation)



        

###################################################
#################### Main method ##################
###################################################


def main():
       
        ##### create a window, canvas
        root = Tk() # instantiate a tkinter window
        nrow=40
        ncol=40
        scale=20
        canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black") # create a canvas width*height
        canvas.pack()

        ### general binding events to choose a testing function
        root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
        root.bind("2",lambda e:test2(canvas,nrow,ncol,scale))
        root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
        root.bind("4",lambda e:test4(root,canvas,nrow,ncol,scale))
        root.bind("5",lambda e:test5(root,canvas,nrow,ncol,scale))
        root.bind("<d>",lambda e:delete_all(canvas))
        
       
        
        root.mainloop() # wait until the window is closed
        
if __name__=="__main__":
    main()

