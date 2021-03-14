######-General TODOs-######
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
smile = pygame.image.load("resources/smile.png")
smiledead = pygame.image.load("resources/smiledead.png")
smilepressed = pygame.image.load("resources/smilepressed.png")
smilewin = pygame.image.load("resources/smilewin.png")

smile = pygame.transform.scale(smile, (40, 40))
smiledead = pygame.transform.scale(smiledead, (40, 40))
smilepressed = pygame.transform.scale(smilepressed, (40, 40))
smilewin = pygame.transform.scale(smilewin, (40, 40))

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
        self.smileImages = {}

        self.grid = []

        self.screen = pygame.display.set_mode(self.size)

        # Flag limit
        self.flagCounter = 10

        self.mined = False
        self.isWin = False

        # Enables or disables debug mode
        self.isDebug = False

        # Used for when the button is pressed
        # Indicates to the draw() method that the button is being pressed so it shows the corresponding image
        # Very janky solution
        self.held = False

        # Initial click check
        self.initClick = False

    def run(self):
        pygame.init()
        running = True
        pygame.display.set_caption("Pymine") # It's not blind anymore yay
        pygame.display.set_icon(pygame.image.load('resources/bomb.png'))
        self.grid = Board.getGrid(Board)  
        self.loadImage()          
        self.draw()

        start_time = 0

        if (self.isDebug == True):
           self.debug()
           
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
                elif (event.type == pygame.MOUSEBUTTONDOWN):

                    # Press the button to reset/restart game
                    smile_rect = smile.get_rect(topleft=(80, 205))
                    if smile_rect.collidepoint(event.pos):
                        self.held = True
                        self.reset()

                    if (self.isDebug):
                        print(f"Coordinates are: {pygame.mouse.get_pos()}")
                    
                    # Finds out which tile the mouse clicked on
                    x = Tile().mouseClickX(self.width, self.margin)
                    y = Tile().mouseClickY(self.height, self.margin)

                    # Ignore any input outside of grid (aka anything outside the grid is not grid therefore ignore)
                    if (not Board().inboundChecker(x, y)):
                        continue        
                    # Once the game is done, no other input on the board should be accepted
                    if (Board().inboundChecker and self.mined or Board().inboundChecker and self.isWin):
                        continue

                    # If first click is a mine, move it to one of the corners of the grid
                    if(not self.initClick):
                        if (event.button == 1 and self.grid[x][y].mine):
                            self.grid[x][y].mine = False
                            
                            if (self.grid[0][0].mine == False):
                                self.grid[0][0].mine = True
                            elif (self.grid[0][9].mine == False):
                                self.grid[0][9].mine = True
                            elif (self.grid[9][0].mine == False):
                                self.grid[9][0].mine = True
                            else:
                                self.grid[9][9].mine = True
                        self.initClick = True

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

                # Return the button to normal once mouse input is done 
                self.held = False

            ## Closes the game after a delay of 2 seconds when won
            if (self.isGridCleared()):
                self.isWin = True

            # Reveals the mines and closes after a delay of 5 seconds
            if (self.mined):
                Board().revealGrid(self.grid) 
                self.draw()
                pygame.display.flip()

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

        # Default button image
        self.screen.blit(smile, (80, 205))

        # Show different button states depending on condition
        if (self.mined):
            self.screen.blit(smiledead, (80, 205))
        elif (self.isWin):
            self.screen.blit(smilewin, (80, 205))
        elif (self.held):
            self.screen.blit(smilepressed, (80, 205))

        for x in range(10):
            for y in range(10):
                
                # Will apply a different image depending on tile state
                image = self.images[self.getTileImg(self.grid[y][x])] 
                self.screen.blit(image, tLeft)
                tLeft = (tLeft[0] + self.tileSize[0], tLeft[1])

            tLeft = (0, tLeft[1] + self.tileSize[1])
        font = pygame.font.SysFont('Arial', 24)
        flagCounter = font.render(str(self.flagCounter), True, (0, 0, 0))
        self.screen.blit(flagCounter, (150, 210))

    # Debug mode which reveals mines
    def debug(self):
        Board().revealGrid(self.grid)
        self.draw()

    # Resets the game, typically when a game is won or lost
    def reset(self):
        self.isWin = False
        self.mined = False
        self.flagCounter = 10

        Board.makeGrid(Board)
        self.grid = Board.getGrid(Board)

        if (self.isDebug == True):
           self.debug()

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


