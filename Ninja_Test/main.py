import pygame
import sys
import random
import math
import heapq
from typing import List, Tuple, Dict

# Константы игры
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
GRID_SIZE = 20
COLORS = {
    'floor': (200, 200, 200),    # 0 - пол
    'wall': (50, 50, 50),        # 1 - стена
    'table': (139, 69, 19),      # 2 - стол
    'chair': (160, 82, 45),      # 3 - стул
    'printer': (70, 130, 180),   # 4 - принтер
    'door': (210, 180, 140),     # 5 - дверь
    'player': (0, 255, 0),       # Игрок
    'enemy': (255, 0, 0)         # Враг
}

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Office Escape")
        self.clock = pygame.time.Clock()
        
        # Загрузка уровня из файла
        self.level = self._load_level("Level_2.txt")
        self.obstacles = [1, 2, 3, 4, 5]  # Непроходимые объекты

         # Поиск пути
        self.pathfinder = Pathfinder(self.level, self.obstacles)

        # Игровые объекты
        self.player = Player(self._find_free_position())
        self.enemies = []
        self._spawn_enemies(50)  # Можно задать любое количество врагов
        


    def _load_level(self, filename):
        #Загрузка уровня из файла с обработкой разных кодировок#
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                level_str = content.split('=', 1)[1].strip()
                return eval(level_str)
        except UnicodeDecodeError:
            with open(filename, 'r', encoding='cp1251') as file:
                content = file.read()
                level_str = content.split('=', 1)[1].strip()
                return eval(level_str)

    def _find_free_position(self):
        #Поиск свободной позиции на полу#
        while True:
            x = random.randint(0, len(self.level[0])-1)
            y = random.randint(0, len(self.level)-1)
            if self.level[y][x] == '0':
                return x * GRID_SIZE, y * GRID_SIZE

    def _spawn_enemies(self, count):
        #Создание врагов без наложения#
        for _ in range(count):
            while True:
                pos = self._find_free_position()
                
                # Проверка расстояния до игрока и других врагов
                valid = True
                if math.hypot(pos[0]-self.player.x, pos[1]-self.player.y) < 100:
                    valid = False
                
                for enemy in self.enemies:
                    if math.hypot(pos[0]-enemy.x, pos[1]-enemy.y) < GRID_SIZE*2:
                        valid = False
                        break
                
                if valid:
                    self.enemies.append(Enemy(pos[0], pos[1], self.pathfinder))
                    break

    def run(self):
        #Основной игровой цикл#
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Обновление
            self.player.update(self.level, self.obstacles)
            
            # Обновляем только ближайших врагов
            active_enemies = []
            for enemy in self.enemies:
                dist = math.hypot(enemy.x-self.player.x, enemy.y-self.player.y)
                if dist < 200:  # Враги активируются только рядом с игроком
                    enemy.update(self.player, self.level, self.enemies)
                    active_enemies.append(enemy)
                else:
                    active_enemies.append(enemy)  # Но сохраняем всех врагов
            
            self.enemies = active_enemies
            
            # Отрисовка
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)

    def _draw(self):
        #Отрисовка игры#
        self.screen.fill((0, 0, 0))
        
        # Отрисовка уровня
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if cell == '0':
                    pygame.draw.rect(self.screen, COLORS['floor'], rect)
                elif cell == '1':
                    pygame.draw.rect(self.screen, COLORS['wall'], rect)
                elif cell == '2':
                    pygame.draw.rect(self.screen, COLORS['table'], rect)
                elif cell == '3':
                    pygame.draw.rect(self.screen, COLORS['chair'], rect)
                elif cell == '4':
                    pygame.draw.rect(self.screen, COLORS['printer'], rect)
                elif cell == '5':
                    pygame.draw.rect(self.screen, COLORS['door'], rect)
        
        # Отрисовка игрока и врагов
        pygame.draw.rect(self.screen, COLORS['player'], 
                        (self.player.x, self.player.y, GRID_SIZE, GRID_SIZE))
        
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, COLORS['enemy'], 
                           (enemy.x, enemy.y, GRID_SIZE, GRID_SIZE))

class Pathfinder:
    #Поиск пути с оптимизацией#
    def __init__(self, level, obstacles):
        self.level = level
        self.obstacles = obstacles
        self.width = len(level[0])
        self.height = len(level)
    
    def find_path(self, start, end):
        #Упрощенный поиск пути для оптимизации#
        # В этой версии враги идут напрямую к игроку, но с избеганием препятствий
        return []

class Player:
    #Класс игрока с точной коллизией#
    def __init__(self, pos):
        self.x, self.y = pos
        self.speed = 5
        self.rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
    
    def update(self, level, obstacles):
        keys = pygame.key.get_pressed()
        old_x, old_y = self.x, self.y
        
        # Движение
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Обновляем rect для коллизий
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверка коллизий со стенами и объектами
        if self._check_collision(level, obstacles):
            self.x, self.y = old_x, old_y
            self.rect.x = self.x
            self.rect.y = self.y
    
    def _check_collision(self, level, obstacles):
        #Проверка столкновений со всеми препятствиями#
        grid_x = int(self.x // GRID_SIZE)
        grid_y = int(self.y // GRID_SIZE)
        
        # Проверяем все клетки, которые пересекает игрок
        for y in range(max(0, grid_y-1), min(len(level), grid_y+2)):
            for x in range(max(0, grid_x-1), min(len(level[0]), grid_x+2)):
                if level[y][x] in [str(o) for o in obstacles]:
                    obj_rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if self.rect.colliderect(obj_rect):
                        return True
        return False

class Enemy:
    #Класс врага с избеганием столкновений#
    def __init__(self, x, y, pathfinder):
        self.x, self.y = x, y
        self.speed = 2
        self.pathfinder = pathfinder
        self.path = []
        self.rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        self.avoid_radius = GRID_SIZE * 2  # Радиус избегания других врагов
    
    def update(self, player, level, enemies):
        # Движение только если игрок близко
        dist_to_player = math.hypot(player.x - self.x, player.y - self.y)
        if dist_to_player > 300:  # Не двигаемся если игрок далеко
            return
        
        old_x, old_y = self.x, self.y
        
        # Базовое движение к игроку
        dx = player.x - self.x
        dy = player.y - self.y
        if dist_to_player > 0:
            dx, dy = dx/dist_to_player, dy/dist_to_player
        
        # Избегание других врагов
        for other in enemies:
            if other is not self:
                dist = math.hypot(other.x - self.x, other.y - self.y)
                if dist < self.avoid_radius:
                    avoid_dx = self.x - other.x
                    avoid_dy = self.y - other.y
                    if dist > 0:
                        avoid_dx = (avoid_dx/dist) * (self.avoid_radius - dist)/self.avoid_radius
                        avoid_dy = (avoid_dy/dist) * (self.avoid_radius - dist)/self.avoid_radius
                    dx += avoid_dx * 0.5
                    dy += avoid_dy * 0.5
        
        # Нормализация вектора движения
        if math.hypot(dx, dy) > 0:
            dx, dy = dx/math.hypot(dx, dy), dy/math.hypot(dx, dy)
        
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверка коллизий (аналогично игроку)
        if self._check_collision(level):
            self.x, self.y = old_x, old_y
            self.rect.x = self.x
            self.rect.y = self.y
    
    def _check_collision(self, level):
        #Проверка столкновений с препятствиями#
        grid_x = int(self.x // GRID_SIZE)
        grid_y = int(self.y // GRID_SIZE)
        
        for y in range(max(0, grid_y-1), min(len(level), grid_y+2)):
            for x in range(max(0, grid_x-1), min(len(level[0]), grid_x+2)):
                if level[y][x] in ['1', '2', '3', '4', '5']:
                    obj_rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if self.rect.colliderect(obj_rect):
                        return True
        return False

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()