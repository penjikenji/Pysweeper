######-General TODOs-######
# TODO: Add smiley for win/lose/reset indicator
# TODO: Add time and flag counter???
# TODO: Cleaning up the mess
# TODO: Beat minesweeper
######---------------######
# TODO Line 111: Implement a debug mode
######-Suggestions-########
# Limited number of flags (An array of counters that only reaches up to 10? Then when it is unchecked it is removed using pop())
# Un-hard code everything
# Minimize size of tiles/resolution
# Menubar for reset/difficulty/etc. (May require either pygame-gui or pygame-menu)

import pygame
import os
from random import randint

from board import Board
from tile import Tile
import time

# mmmm constants
GRAY = (140, 138, 137)

class Main():
    def __init__(self, size = [200, 250], width = 19, height = 19, margin = 1):

        self.size = size                     
        self.width = width      
        self.height = height
        self.margin = margin

        # Find size of each tile for images
        # Load images into a dictionary
        self.tileSize = (self.size[0] // 10, 200 // 10)
        self.images = {}

        self.grid = []

        self.screen = pygame.display.set_mode(self.size)

        self.flagCounter = 10
        self.mined = False
        self.isWin = False

        # Enables or disables debug mode
        self.isDebug = False

    def run(self):
        pygame.init()
        running = True
        pygame.display.set_caption("Pymine") # It's not blind anymore yay
        pygame.display.set_icon(pygame.image.load('resources/bomb.png'))
        self.grid = Board.getGrid(Board)  
        self.loadImage()          
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

                    # Ignore any input outside of grid 
                    if (not Board().inboundChecker(x, y)):
                        continue

                    # Tile is flagged/unflagged when user right clicks on tile
                    # continue is used becase mine does not need to be checked
                    if (event.button == 3 and self.grid[x][y].flagged == False and self.flagCounter > 0):
                        self.grid[x][y].flagged = True
                        self.flagCounter -= 1
                        continue

                    if (event.button == 3 and self.grid[x][y].flagged):
                        self.grid[x][y].flagged = False
                        self.flagCounter += 1

                    if (event.button == 1):

                        # Returns true if there is a mine beneath the revealed tile
                        if (Board().isMineHit(self.grid, x, y)):
                            self.grid[x][y].visible = True
                            self.mined = True
                            continue
                        else:

                            #Searches for tiles with adjacent mines and does a flood fill(?) of tiles with no adjacent mines
                            Board().search(self.grid, x, y)
                    
            # Closes the game after a delay of 2 seconds when won
            if (self.isGridCleared()):
                time.sleep(2)
                running = False

            # Reveals the mines and closes after a delay of 5 seconds
            elif (self.mined):
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
        tLeft = (0, 0) # Used to append an image onto each tile using coordinates
        self.screen.fill(GRAY)
        for x in range(10):
            for y in range(10):

                # Will apply a different image depending on tile state
                image = self.images[self.getTileImg(self.grid[y][x])] 
                self.screen.blit(image, tLeft)

                tLeft = (tLeft[0] + self.tileSize[0], tLeft[1])

            tLeft = (0, tLeft[1] + self.tileSize[1])

    # Debug mode which reveals mines and user input in the terminal, including an option to reload a new grid
    # TODO: Actually implement this better (Do a reveal all?)
    def debug(self):
        for x in range(10):
            for y in range(10):
                if (self.grid[x][y].mine):
                    print(f"Mines are placed at {x} {y}")
            Board().revealGrid(self.grid)
            self.draw()

    # Resets the game, typically when a game is won or lost
    def reset(self):
        self.makeGrid()
        self.genMines()
        self.draw()

    # Will return true if every single block that is checked returns 1 aka is clicked
    def isGridCleared(self):
        for x in range(10):
            for y in range(10):
                if (not self.grid[x][y].visible):
                    return False
        return True

    # Loads images from resources folder into a dict
    def loadImage(self):
        for file in os.listdir("resources"):
            if (not file.endswith(".png")):
                continue
            image = pygame.image.load(r"resources/" + file)
            image = pygame.transform.scale(image, self.tileSize)
            self.images[file.split(".")[0]] = image

    # Gets the image from dict depending on tile state
    def getTileImg(self, tile):
        if (tile.mine and tile.visible):
            return "bomb"
        
        if (not tile.mine and tile.visible and tile.numAdj == 0):
            return "blankblock"
       
        if (tile.flagged):
            return "flag"
        
        if (tile.visible and tile.numAdj > 0):
            return f"block{tile.numAdj}"

        return "block"
    
minesweeper = Main()
minesweeper.run()


