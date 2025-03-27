import pygame
import sys
import random
import math
import heapq
from typing import List, Tuple, Set, Dict

# Константы игры
SCREEN_SIZE = (1200, 800)  # Размеры игрового окна
COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'gray': (100, 100, 100)
}

class Game:
    #Главный класс игры, управляющий всеми процессами
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Ninja Game")  # Название игры
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Шрифт для текста
        
        # Состояния игры: running/paused/game_over
        self.state = 'running'
        
        # Группы спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self._initialize_game()  # Инициализация игровых объектов

    def _initialize_game(self):
        #Инициализация всех игровых объектов#
        self._create_walls()  # Создание стен
        self.pathfinder = Pathfinder(self.walls)  # Инициализация поиска пути
        self.player = Player(100, 100)  # Создание игрока
        self.all_sprites.add(self.player)
        self._spawn_enemies(4)  # Спавн 4 врагов

    def _create_walls(self):
        #Создание стен уровня#
        wall_layout = [
            # Границы экрана
            [0, 0, SCREEN_SIZE[0], 20],
            [0, 0, 20, SCREEN_SIZE[1]],
            [0, SCREEN_SIZE[1]-20, SCREEN_SIZE[0], 20],
            [SCREEN_SIZE[0]-20, 0, 20, SCREEN_SIZE[1]],
            # Внутренние стены
            [300, 100, 20, 200],
            [400, 300, 200, 20],
            [600, 200, 20, 300]
        ]
        
        # Создание стен из шаблона
        for x, y, w, h in wall_layout:
            wall = Wall(x, y, w, h)
            self.walls.add(wall)
            self.all_sprites.add(wall)

    def _spawn_enemies(self, count: int):
        #Создание врагов с проверкой позиции#
        for _ in range(count):
            while True:  # Поиск свободной позиции
                pos = (
                    random.randint(100, SCREEN_SIZE[0]-100),
                    random.randint(100, SCREEN_SIZE[1]-100)
                )
                if not self._position_blocked(pos, 20):
                    break
                    
            enemy = Enemy(*pos, self.pathfinder)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def _position_blocked(self, pos: Tuple[int, int], size: int) -> bool:
        #Проверка, занята ли позиция стенами#
        temp_rect = pygame.Rect(pos[0], pos[1], size, size)
        return any(temp_rect.colliderect(wall.rect) for wall in self.walls)

    def run(self):
        #Главный игровой цикл#
        while True:
            self._handle_events()  # Обработка ввода
            if self.state == 'running':
                self._update()  # Обновление состояния
            self._render()  # Отрисовка
            self.clock.tick(60)  # 60 FPS

    def _handle_events(self):
        #Обработка событий игры#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and self.state == 'game_over':
                    self._reset_game()  # Рестарт игры

    def _update(self):
        #Обновление игрового состояния#
        self.player.update(self.walls)  # Обновление игрока
        
        # Обновление врагов
        for enemy in self.enemies:
            enemy.update(self.player, self.walls, self.enemies)
        
        # Проверка коллизий
        self._check_enemy_collisions()  # Столкновение с врагами

    def _check_enemy_collisions(self):
        #Обработка столкновений с врагами#
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.state = 'game_over'

    def _reset_game(self):
        #Сброс игры в начальное состояние#
        self.state = 'running'
        # Очистка всех спрайтов
        self.all_sprites.empty()
        self.walls.empty()
        self.enemies.empty()
        self._initialize_game()  # Повторная инициализация

    def _render(self):
        #Отрисовка игрового кадра#
        self.screen.fill(COLORS['black'])  # Черный фон
        self.all_sprites.draw(self.screen)  # Отрисовка всех спрайтов
        self._draw_ui()  # Отрисовка интерфейса
        pygame.display.flip()  # Обновление экрана

    def _draw_ui(self):
        #Отрисовка пользовательского интерфейса#
        # Сообщения о конце игры
        if self.state == 'game_over':
            text = self.font.render("Game Over! Press R to restart", True, COLORS['red'])
            self.screen.blit(text, (SCREEN_SIZE[0]//2 - 150, SCREEN_SIZE[1]//2))


class Pathfinder:
    #Класс для поиска пути с использованием алгоритма A*#
    def __init__(self, walls, grid_size=20):
        self.grid_size = grid_size
        self.obstacle_grid = self._build_obstacle_grid(walls)  # Сетка препятствий
    
    def _build_obstacle_grid(self, walls) -> List[List[bool]]:
        #Построение сетки препятствий для поиска пути#
        grid_width = SCREEN_SIZE[0] // self.grid_size
        grid_height = SCREEN_SIZE[1] // self.grid_size
        grid = [[False for _ in range(grid_height)] for _ in range(grid_width)]
        
        # Заполнение сетки данными о стенах
        for wall in walls:
            left = wall.rect.left // self.grid_size
            right = wall.rect.right // self.grid_size
            top = wall.rect.top // self.grid_size
            bottom = wall.rect.bottom // self.grid_size
            
            for x in range(left, right + 1):
                for y in range(top, bottom + 1):
                    if 0 <= x < grid_width and 0 <= y < grid_height:
                        grid[x][y] = True
        return grid
    
    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        #Поиск пути от start до end#
        start_node = self._world_to_grid(start)
        end_node = self._world_to_grid(end)
        
        if not self._valid_node(end_node):
            return []  # Невозможно дойти до цели
        
        open_set = []
        heapq.heappush(open_set, (0, start_node))
        came_from = {}
        g_score = {start_node: 0}
        f_score = {start_node: self._heuristic(start_node, end_node)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == end_node:
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, end_node)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return []  # Путь не найден

    def _world_to_grid(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        #Конвертация координат мира в координаты сетки#
        return (pos[0] // self.grid_size, pos[1] // self.grid_size)

    def _valid_node(self, node: Tuple[int, int]) -> bool:
        #Проверка, доступен ли узел сетки#
        x, y = node
        return (0 <= x < len(self.obstacle_grid) and 
                0 <= y < len(self.obstacle_grid[0]) and 
                not self.obstacle_grid[x][y])

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        #Эвристика для A* (манхэттенское расстояние)#
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        #Получение соседних доступных узлов#
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Вверх, вправо, вниз, влево
        neighbors = []
        
        for dx, dy in directions:
            neighbor = (node[0] + dx, node[1] + dy)
            if self._valid_node(neighbor):
                neighbors.append(neighbor)
                
        return neighbors

    def _reconstruct_path(self, came_from: Dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        #Восстановление пути от текущей позиции до старта#
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class Wall(pygame.sprite.Sprite):
    #Класс стены - непроходимое препятствие#
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(COLORS['blue'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    #Класс игрока#
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(COLORS['green'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5  # Скорость движения
        
    def update(self, walls):
        #Обновление позиции игрока#
        keys = pygame.key.get_pressed()
        old_x, old_y = self.rect.x, self.rect.y
        
        # Движение по клавишам
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            
        # Проверка столкновений со стенами
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x, self.rect.y = old_x, old_y


class Enemy(pygame.sprite.Sprite):
    #Класс врага с интеллектом#
    def __init__(self, x, y, pathfinder):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(COLORS['red'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2  # Скорость врага
        self.path = []  # Текущий путь
        self.pathfinder = pathfinder  # Объект поиска пути
        self.recalculate_counter = 0  # Счетчик для перерасчета пути
        self.avoid_radius = 50  # Радиус избегания других врагов
    
    def update(self, player, walls, enemies):
        #Обновление позиции врага#
        self.recalculate_counter += 1
        
        # Перерасчет пути не каждый кадр для оптимизации
        if self.recalculate_counter >= 20 or not self.path:
            self.recalculate_counter = 0
            self.path = self.pathfinder.find_path(
                (self.rect.centerx, self.rect.centery),
                (player.rect.centerx, player.rect.centery)
            )
        
        if self.path:
            # Движение по пути
            next_node = self.path[0]
            target_x = next_node[0] * self.pathfinder.grid_size + self.pathfinder.grid_size // 2
            target_y = next_node[1] * self.pathfinder.grid_size + self.pathfinder.grid_size // 2
            
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.hypot(dx, dy)
            
            if distance < 5:  # Достигли узла пути
                if len(self.path) > 1:
                    self.path.pop(0)
            else:
                if distance > 0:
                    dx = dx / distance
                    dy = dy / distance
                
                # Избегание других врагов
                for enemy in enemies:
                    if enemy != self:
                        enemy_dist = math.hypot(enemy.rect.centerx - self.rect.centerx, 
                                              enemy.rect.centery - self.rect.centery)
                        if enemy_dist < self.avoid_radius:
                            avoid_dx = self.rect.centerx - enemy.rect.centerx
                            avoid_dy = self.rect.centery - enemy.rect.centery
                            if enemy_dist > 0:
                                avoid_dx = avoid_dx / enemy_dist * (self.avoid_radius - enemy_dist) / self.avoid_radius
                                avoid_dy = avoid_dy / enemy_dist * (self.avoid_radius - enemy_dist) / self.avoid_radius
                            dx += avoid_dx * 0.5
                            dy += avoid_dy * 0.5
                
                # Нормализация вектора движения
                if math.hypot(dx, dy) > 0:
                    dx = dx / math.hypot(dx, dy)
                    dy = dy / math.hypot(dx, dy)
                
                old_x, old_y = self.rect.x, self.rect.y
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
                
                # Проверка столкновений со стенами
                if pygame.sprite.spritecollide(self, walls, False):
                    self.rect.x, self.rect.y = old_x, old_y
                    self.path = []  # При столкновении пересчитываем путь


if __name__ == "__main__":
    game = Game()
    game.run()