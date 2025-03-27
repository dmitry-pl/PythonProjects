import pygame

pygame.init()

class Button:

    def __init__(self, x, y, width, height, image, img_sel):

        self.image = pygame.image.load(image)
        self.image_select = pygame.image.load(img_sel)
        self.img_basic = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.rect.x and pos[0] < self.rect.x + self.width:
            if pos[1] > self.rect.y and pos[1] < self.rect.y + self.height:
                return True
        return False



    def draw(self, win, pos, outline=None):
        # Call this method to draw the button on the screen
        if not self.isOver(pos):
            win.blit(self.image, self.rect)
        else:
            win.blit(self.image_select, self.rect)

        



    