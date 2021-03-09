######-TODOs-######
# TODO line 13: Different preset grid sizes depending on difficulty? (implement a self.tileAmount)
# TODO line 27: Use an array of objects instead of integers?
######-------######



import pygame
from random import randint

# Static variables for color
class Board():
    def __init__(self):
        self.mines = 10 # Really don't need this tbh
        self.grid = []
    # A list comphrehension that makes a 9x9 2D array for the grid
    # TODO: Different preset grid sizes depending on difficulty? (implement a self.tileAmount)
    def makeGrid(self):
        self.grid = [[0 for x in range(10)] for x in range(10)]
   
    # Makes some mines
    # TODO: depending on the size of the grid, up the amount of mines?
    # Or just have a set amount depending the size of grid
    def makeMines(self):
        for i in range(10):
            x = randint(0, 9)
            y = randint(0, 9)
            self.grid[x][y] = 100           # TODO: Use an array of objects instead of integers? 
                                            # Mines are set as 100 since proximity from last revealed tile can't reach that far

    def revealGrid(self, grid):
        for x in range(10):
            for y in range(10):
                if (grid[x][y] == 100):
                    grid[x][y] = 101

    def getGrid(self):
        return self.grid

Board.makeGrid(Board)
Board.makeMines(Board)


