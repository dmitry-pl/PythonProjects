import pygame
from pathfinding import Grid, a_star_search

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.mana = 0
        self.attack_damage = 20
        self.shadow_clone_cooldown = 0
        self.level = 1
        self.exp = 0

    def update(self, level, enemies):
        # Движение игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Атака
        if keys[pygame.K_a]:
            self.attack(enemies)

        # Проверка на создание теневого клона
        if keys[pygame.K_SPACE] and self.mana >= 50 and self.shadow_clone_cooldown <= 0:
            self.mana -= 50
            self.shadow_clone_cooldown = 300  # Время перезарядки
            return ShadowClone(self.x, self.y, self.attack_damage // 2)
        return None

    def attack(self, enemies):
        # Атака ближайшего врага
        for enemy in enemies:
            if abs(self.x - enemy.x) < 50 and abs(self.y - enemy.y) < 50:
                enemy.take_damage(self.attack_damage)
                if enemy.health <= 0:
                    self.exp += 10
                    self.mana += 5

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def level_up(self):
        if self.exp >= 100:
            self.level += 1
            self.exp = 0
            self.max_health += 20
            self.health = self.max_health
            self.attack_damage += 10
            return True
        return False

    def draw(self, screen):
        # Отрисовка игрока (квадрат)
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, 40, 40))

class ShadowClone:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.speed = 4
        self.health = 50
        self.damage = damage
        self.state = "follow"  # Начальное состояние
        self.grid = Grid(20, 15)

    def update(self, player, enemies):
        if self.state == "follow":
            self.follow(player)
            for enemy in enemies:
                if abs(self.x - enemy.x) < 50 and abs(self.y - enemy.y) < 50:
                    self.state = "attack"
                    break
        elif self.state == "attack":
            target = self.find_nearest_enemy(enemies)
            if target:
                self.attack(target)
            else:
                self.state = "follow"

    def follow(self, player):
        # Используем A* для поиска пути к игроку
        start = (self.x // 40, self.y // 40)
        goal = (player.x // 40, player.y // 40)
        path = a_star_search(self.grid, start, goal)
        if path:
            next_step = path[0]
            self.x = next_step[0] * 40
            self.y = next_step[1] * 40

    def attack(self, enemy):
        enemy.take_damage(self.damage)

    def find_nearest_enemy(self, enemies):
        nearest = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = abs(self.x - enemy.x) + abs(self.y - enemy.y)
            if distance < min_distance:
                min_distance = distance
                nearest = enemy
        return nearest

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 0, 128), (self.x, self.y, 40, 40))