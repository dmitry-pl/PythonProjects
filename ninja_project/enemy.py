import random
import pygame
from pathfinding import Grid, a_star_search

class Enemy:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.speed = 2 if type == "melee" else 1
        self.health = 50 if type == "melee" else 30
        self.damage = 10 if type == "melee" else 5
        self.state = "idle"  # Начальное состояние
        self.grid = Grid(20, 15)

    @staticmethod
    def random_enemy():
        # Случайное создание врага
        type = random.choice(["melee", "ranged"])
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        return Enemy(x, y, type)

    def update(self, player):
        # Переключение состояний
        if self.state == "idle":
            if abs(self.x - player.x) < 200 and abs(self.y - player.y) < 200:
                self.state = "chase"
        elif self.state == "chase":
            self.chase(player)
            if abs(self.x - player.x) < 50 and abs(self.y - player.y) < 50:
                self.state = "attack"
        elif self.state == "attack":
            self.attack(player)
            if abs(self.x - player.x) >= 50 or abs(self.y - player.y) >= 50:
                self.state = "chase"

    def chase(self, player):
        # Используем A* для поиска пути к игроку
        start = (self.x // 40, self.y // 40)
        goal = (player.x // 40, player.y // 40)
        came_from, _ = a_star_search(self.grid, start, goal)

        # Восстанавливаем путь
        path = self.reconstruct_path(came_from, start, goal)
        if path and len(path) > 1:
            next_step = path[1]  # Первый шаг после текущей позиции
            self.x = next_step[0] * 40
            self.y = next_step[1] * 40

    def reconstruct_path(self, came_from, start, goal):
        # Восстанавливаем путь от цели к началу
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()  # Переворачиваем путь, чтобы он шёл от начала к цели
        return path

    def attack(self, player):
        player.take_damage(self.damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def draw(self, screen):
        color = (255, 0, 0) if self.type == "melee" else (255, 165, 0)
        pygame.draw.rect(screen, color, (self.x, self.y, 40, 40))