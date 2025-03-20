import pygame
from player import Player, ShadowClone
from enemy import Enemy
from level import Level
from skills import SkillTree

class Game:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ниндзя будущего")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Инициализация уровня, игрока и врагов
        self.level = Level()
        self.player = Player(100, 100)
        self.shadow_clone = None
        self.enemies = []
        self.skill_tree = SkillTree()

        # Генерация первого уровня
        self.generate_level(1)

    def generate_level(self, level_number):
        # Генерация уровня и врагов
        self.level.generate()
        self.enemies = [Enemy.random_enemy() for _ in range(5 + level_number * 2)]

    def run(self):
        # Основной игровой цикл
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
                self.draw()
            self.clock.tick(60)

    def handle_events(self):
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Пауза
                    self.paused = not self.paused

    def update(self):
        # Обновление состояния игры
        self.player.update(self.level, self.enemies)
        if self.shadow_clone:
            self.shadow_clone.update(self.player, self.enemies)
        for enemy in self.enemies:
            enemy.update(self.player)

        # Удаление мертвых врагов
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

        # Проверка на повышение уровня
        if self.player.level_up():
            print(f"Уровень повышен! Теперь уровень {self.player.level}")

    def draw(self):
        # Отрисовка игры
        self.screen.fill((0, 0, 0))  # Черный фон
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        if self.shadow_clone:
            self.shadow_clone.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.flip()

    def pause(self):
        # Пауза
        pass  # Можно добавить меню паузы

    def game_over(self):
        # Конец игры
        pass  # Можно добавить экран завершения игры