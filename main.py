######-General TODOs-######
# TODO: Be able to reveal adjacent blank tiles upon clicking on a tile
# TODO: ^^^ Show numbers on revealed tiles ^^^ (How did i forget this)
# TODO: These classes are still unorganized 
# TODO: Replace drawn tiles with assets from WinXP game (May just use pygame-gui to show a separate window with Microsoft BOB)
# TODO: ^^^ Microsoft BOB will be the indicator for win or game over ^^^
# TODO: Menubar for reset/difficulty/etc. (May require either pygame-gui or pygame-menu)
# TODO: Cleaning up the mess
# TODO: Beat minesweeper
######---------------######
# TODO Line 65: Be able to uncheck a flagged block
# TODO Line 111: Implement a debug mode
######-Suggestions-########
# Use objects instead of ints
# Limited number of flags (An array of counters that only reaches up to 10? Then when it is unchecked it is removed using pop())
# Un-hard code everything
# Minimize size of tiles/resolution

import pygame
from random import randint

from board import Board
from tile import Tile
import time

# mmmm constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (140, 138, 137)
RED = (255, 0, 0)
PURPLE = (167, 66, 245)

class Main():
    def __init__(self, size = [250, 250], width = 24, height = 24, margin = 1):

        self.size = size        # There's an "error" here because sonarlint says I'm not following code conventions (python:S5717)             
        self.width = width      # Shut up sonarlint i can do whatever i want
        self.height = height
        self.margin = margin

        self.grid = []

        self.screen = pygame.display.set_mode(self.size)

        self.mined = False
        self.isWin = False

        # Enables or disables debug mode
        self.isDebug = False

    def run(self):
        pygame.init()
        running = True
        pygame.display.set_caption("Blindsweeper")  # It's called Blindsweeper because you can't see past a block and they aren't numbered (yet)
        pygame.display.set_icon(pygame.image.load('resources/bomb.png'))
        self.grid = Board.getGrid(Board)            # I think there's a better way to implement this and it starts with inheritence
        self.draw()

        if (self.isDebug == True):
           self.debug()

        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                elif (event.type == pygame.MOUSEBUTTONDOWN):

                    # Finds out which tile the mouse clicked on
                    x = Tile().mouseClickX(self.width, self.margin)
                    y = Tile().mouseClickY(self.height, self.margin)

                    # TODO: be able to uncheck a flagged tile (might be time to switch to using objects instead of ints)
                    # If the user right clicks, it flags the tile
                    # continue is used becase mine does not need to be checked
                    if (event.button == 3):
                        self.grid[x][y] = 200
                        continue

                    # Returns true if there is a mine beneath the revealed tile
                    if (Tile().isMineHit(self.grid, x, y)):
                        self.grid[x][y] = 101
                        self.mined = True
                    else:
                        self.grid[x][y] = 1
                        Tile().searchAdjMine(self.grid)

                
            
            # Closes the game after a delay of 2 seconds when won
            if (self.isGridCleared() == True):
                time.sleep(2)
                running = False

            # Reveals the mines and closes after a delay of 5 seconds
            elif (self.mined == True):
                Board().revealGrid(self.grid) 
                self.draw()
                pygame.display.flip()
                time.sleep(2)
                running = False

            # Run and update the game at a lock of 60fps
            self.draw()
            clock = pygame.time.Clock()
            clock.tick(60)
            pygame.display.flip()
        pygame.quit()

    # Draws the grid and colors in tiles for user input
    def draw(self):
        self.screen.fill(BLACK)
        for x in range(10):
            for y in range(10):
                color = WHITE
                if self.grid[y][x] == 1:
                    color = GRAY
                elif self.grid[y][x] == 101:
                    color = RED
                elif self.grid[y][x] == 200:
                    color = PURPLE

                # This makes all the tiles
                pygame.draw.rect(self.screen, color, [(self.margin + self.width) * y + self.margin, 
                                                    (self.margin + self.height) * x + self.margin, 
                                                    self.height, self.width])

    # Debug mode which reveals mines and user input in the terminal, including an option to reload a new grid
    # TODO: Actually implement this better (Do a reveal all?)
    def debug(self):
        for x in range(10):
            for y in range(10):
                if (self.grid[x][y] == 100):
                    print(f"Mines are placed at {x} {y}")

    # Resets the game, typically when a game is won or lost
    def reset(self):
        self.makeGrid()
        self.genMines()
        self.draw()

    # Will return true if every single block that is checked returns 1 aka is clicked
    def isGridCleared(self):
        for x in range(10):
            for y in range(10):
                if (self.grid[x][y] == 0):
                    return False
        return True

minesweeper = Main()
minesweeper.run()

