import pygame
from player_class import *

class Boss():
    def __init__(self):
        self.health = 2500
        self.rect = pygame.Rect(len(level4) * 50 - 800 ,750, 200, 300)

    def update(self, dis, player):
        pygame.draw.rect(dis, (225, 0, 0), (500, 150, self.health // 4, 50))
        dis.blit(pygame.surface.Surface((200, 300)).fill((225, 0, 0)), self.rect)

        for b in player.bullet_list:
            if self.rect.colliderect(b):
                self.health -= player.damage