import pygame
from tile import Tile
from random import randint

class Board():
    def __init__(self):
        self.mines = 10
        self.grid = []

    # A list comphrehension that makes a 9x9 2D array for the grid
    def makeGrid(self):
        self.grid = [[Tile() for x in range(10)] for x in range(10)]
   
    # Makes some mines
    def makeMines(self):
        for i in range(12):
            x = randint(0, 9)
            y = randint(0, 9)
            if (not self.grid[x][y].mine):
                self.grid[x][y].mine = True 
    
    # Reveals mines (used in debug)
    def revealGrid(self, grid):
        for x in range(10):
            for y in range(10):
                if (grid[x][y].mine):
                    grid[x][y].visible = True

    def getGrid(self):
        return self.grid

    # Checks whether or not the tile is in bounds
    # Fixed the out of bounds error because it went by list index, not grid size
    # Grid is 9x9, and the erroneous tiles had indexes of 10
    def inboundChecker(self, x, y):
        if (x >= 0 and x < 10 and y >= 0 and y < 10):
            return True
        return False

    # Checks if user has hit a mine
    def isMineHit(self, grid, x, y):
        if (grid[x][y].mine):
            return True
        return False

    # TODO: This is better in an if-else.. right? I can't remember
    # TODO: That or I have frog brain
    # Searches the adjacent tiles of the clicked tile for mines
    def searchAdjMine(self, grid, x, y):
        adj = 0
        # Search adj north
        if (self.inboundChecker(x - 1, y)):
            if (self.isMineHit(grid, x - 1, y)):
                adj += 1

        # Search adj south
        if (self.inboundChecker(x + 1, y)):
            if (self.isMineHit(grid, x + 1, y)):
                adj += 1

        # Search adj west
        if (self.inboundChecker(x, y - 1)):
            if (self.isMineHit(grid, x, y - 1)):
                adj += 1

        # Search adj east
        if (self.inboundChecker(x, y + 1)):
            if (self.isMineHit(grid, x, y + 1)):
                adj += 1

        # Search north-east
        if (self.inboundChecker(x - 1, y + 1)):
            if (self.isMineHit(grid, x - 1, y + 1)):
                adj += 1

        # Search north-west
        if (self.inboundChecker(x - 1, y - 1)):
            if (self.isMineHit(grid, x - 1, y - 1)):
                adj += 1

        # Search south-east
        if (self.inboundChecker(x + 1, y + 1)):
            if (self.isMineHit(grid, x + 1, y + 1)):
                adj += 1

        # Search south-west
        if (self.inboundChecker(x + 1, y - 1)):
            if (self.isMineHit(grid, x + 1, y - 1)):
                adj += 1

        return adj 

    # Searches neighboring tiles for any blanks and fill 
    def search(self, grid, x, y):

        if (not self.inboundChecker(x, y)):
            return

        tile = grid[x][y]

        if (tile.visible):
            return

        if (tile.mine):
            return 

        numMines = self.searchAdjMine(grid, x, y)
        tile.visible = True

        if numMines > 0:
            grid[x][y].numAdj = numMines
            return

        # Do recursion to search through more tiles 
        self.search(grid, x, y + 1)
        self.search(grid, x, y - 1)
        self.search(grid, x + 1, y)
        self.search(grid, x - 1, y)
        
        
Board.makeGrid(Board)
Board.makeMines(Board)


