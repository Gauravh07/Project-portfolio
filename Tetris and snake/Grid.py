from tkinter import *
from Pixel import Pixel
import numpy as np
import random, time

class Grid:
    """
    Class representing a grid of pixels.
    """

    def __init__(self, root, nrow, ncol, scale):
        """
        Initialize the grid.

        Args:
            root: The root window.
            nrow (int): The number of rows in the grid.
            ncol (int): The number of columns in the grid.
            scale (int): The scale factor for the grid.

        """
        self.nrow = nrow
        self.scale = scale
        self.ncol = ncol
        self.pixels = []
        self.matrix = np.zeros((nrow+1, ncol), dtype=int)

        self.canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="gray")
        self.canvas.pack()

        for i in range(nrow):
            for j in range(ncol):
                x1 = j * scale
                y1 = i * scale
                x2 = x1 + scale
                y2 = y1 + scale
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline='white')

    def random_pixels(self, num_pixels, color):
        """
        Generate random pixels in the grid.

        Args:
            num_pixels (int): The number of random pixels to generate.
            color (int): The color of the random pixels.

        """
        for p in range(num_pixels):
            while True:
                i = np.random.randint(0, self.nrow)
                j = np.random.randint(0, self.ncol)
                if (i, j) not in [(pixel.i, pixel.j) for pixel in self.pixels]:
                    self.addij(i, j, color)
                    break

    def addij(self, i, j, c):
        """
        Add a pixel to the grid at the specified position.

        Args:
            i (int): The row index of the pixel.
            j (int): The column index of the pixel.
            c (int): The color of the pixel.

        """
        if c > 0:
            pixel = Pixel(self.canvas, i, j, self.nrow, self.ncol, self.scale, c)
            self.pixels.append(pixel)
            self.matrix[i, j] = c

            if c == 0:
                print(f"delete {j*self.scale} {i*self.scale} {self.scale} {c} 0")
            else:
                print(f"insert {j*self.scale} {i*self.scale} {self.scale} {c} 0")

    def delij(self, i, j):
        """
        Delete a pixel from the grid at the specified position.

        Args:
            i (int): The row index of the pixel.
            j (int): The column index of the pixel.

        """
        color = self.matrix[i, j]

        if color != 0:
            self.matrix[i, j] = 0
            self.reset()
        else:
            self.flush_row(i)

    def addxy(self, x, y):
        """
        Add a pixel to the grid at the specified (x, y) coordinates.

        Args:
            x (int): The x-coordinate of the pixel.
            y (int): The y-coordinate of the pixel.

        """
        i = y // self.scale
        j = x // self.scale
        self.addij(i, j, 1)

    def delxy(self, x, y):
        """
        Delete a pixel from the grid at the specified (x, y) coordinates.

        Args:
            x (int): The x-coordinate of the pixel.
            y (int): The y-coordinate of the pixel.

        """
        col = x // self.scale
        row = y // self.scale
        if (0 <= col <= self.ncol) and (0 <= row <= self.nrow):
            if self.matrix[row, col] != 0:
                self.matrix[row, col] = 0
                self.reset()
                print("delete %s %s %s %s 1" % (x, y, col, row))
            else:
                print("delete %s %s %s %s 0" % (x, y, col, row))
                self.flush_row(row)

    def reset(self):
        """
        Reset the grid.

        """
        for pixel in self.pixels:
            pixel.delete()

        for i in range(self.nrow):
            for j in range(self.ncol):
                if self.matrix[i, j] != 0 and self.matrix[i, j] >= 0:
                    self.addij(i, j, self.matrix[i, j])

    def flush_row(self, row):
        """
        Flush a row in the grid.

        Args:
            row (int): The index of the row to flush.

        """
        if row < 50:
            pixels = [
                Pixel(self.canvas, row, 0, self.nrow, self.ncol, self.scale, 7, [0, 1]),
                Pixel(self.canvas, row, 1, self.nrow, self.ncol, self.scale, 7, [0, 1]),
                Pixel(self.canvas, row, 2, self.nrow, self.ncol, self.scale, 7, [0, 1]),
                Pixel(self.canvas, row, self.ncol - 1, self.nrow, self.ncol, self.scale, 7, [0, -1]),
                Pixel(self.canvas, row, self.ncol - 2, self.nrow, self.ncol, self.scale, 7, [0, -1]),
                Pixel(self.canvas, row, self.ncol - 3, self.nrow, self.ncol, self.scale, 7, [0, -1])
            ]

            for x in range(10):
                for p in pixels:
                    p.next()
                self.canvas.update()
                time.sleep(0.02)

            for p in pixels:
                p.delete()

        self.matrix[1:row + 1, :] = self.matrix[0:row, :]
        self.matrix[0, :] = 0
        self.reset()


def main():
    """
    Main function to run the Tetris game.
    """
    root = Tk()
    mesh = Grid(root, 50, 30, 20)
    mesh.random_pixels(25, 1)

    root.bind("<Button-1>", lambda e: mesh.addxy(e.x, e.y))
    root.bind("<Button-3>", lambda e: mesh.delxy(e.x, e.y))

    root.mainloop()


if __name__ == "__main__":
    main()
