import pygame

class Tile:
    def __init__(self):
        self.visible = False
        self.mine = False
        self.flagged = False
        self.numAdj = 0

    # Grabs the grid position on x-axis
    def mouseClickX(self, width, margin):
        pos = pygame.mouse.get_pos()

        # Return tile x position
        return pos[0] // (width + margin)

    # Grabs the grid position on y-axis
    def mouseClickY(self, height, margin):
        pos = pygame.mouse.get_pos()

        # Return tile y position
        return pos[1] // (height + margin)