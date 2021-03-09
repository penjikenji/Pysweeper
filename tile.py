######-TODOs-######
# TODO line 9: Make an actual solution to the circular workaround problem
# TODO line 40: frog brain moment (reduce if statement complexity if possible)
# TODO: Manipulate grid based on mine proximity?? Right now it is temp. outputted to terminal
######-------######

from random import randint
import pygame
from board import Board

class Tile: # TODO: Make an actual solution to the circular workaround problem
    def __init__(self, size = [250, 250], width = 24, height = 24, margin = 1):
        self.size = size
        self.width = width
        self.height = height
        self.margin = margin

    def mouseClickX(self, width, margin):
        pos = pygame.mouse.get_pos()

        # Return tile x position
        return pos[0] // (self.width + self.margin)

    def mouseClickY(self, height, margin):
        pos = pygame.mouse.get_pos()

        # Return tile y position
        return pos[1] // (self.height + self.margin)

    # Checks whether or not the tile is in bounds
    def inboundChecker(self, x, y):
        if (x >= 0 and x < self.height and y >= 0 and y < self.width):
            return True
        return False

    # Checks if user has hit a mine
    def isMineHit(self, grid, x, y):
        if grid[x][y] == 100:
            return True
        return False

    # TODO: This is better in an if-else.. right? I can't remember
    # TODO: That or I have frog brain
    # Searches the adjacent tiles of the clicked tile for mines
    def searchAdjMine(self, grid):
        x = self.mouseClickX(self.width, self.margin)
        y = self.mouseClickY(self.height, self.margin)
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

        print(adj) # Testing right now
        return adj 
