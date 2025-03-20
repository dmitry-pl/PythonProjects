import random
import pygame

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def generate_rooms(max_rooms, min_size, max_size):
    rooms = []
    for _ in range(max_rooms):
        width = random.randint(min_size, max_size)
        height = random.randint(min_size, max_size)
        x = random.randint(0, 800 - width)
        y = random.randint(0, 600 - height)
        rooms.append(Room(x, y, width, height))
    return rooms

class Level:
    def __init__(self):
        # Размер уровня в клетках (20x15)
        self.width = 20
        self.height = 15
        self.tiles = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []

    def generate(self):
        # Генерация комнат с использованием BSP
        self.rooms = generate_rooms(5, 4, 8)
        for room in self.rooms:
            # Ограничиваем координаты комнаты в пределах уровня
            room.x = max(0, min(room.x, self.width - room.width))
            room.y = max(0, min(room.y, self.height - room.height))

            # Заполняем стены и пол комнаты
            for x in range(room.x, room.x + room.width):
                for y in range(room.y, room.y + room.height):
                    if x < self.width and y < self.height:  # Проверка на выход за границы
                        if x == room.x or x == room.x + room.width - 1 or y == room.y or y == room.y + room.height - 1:
                            self.tiles[y][x] = 1  # Стены
                        else:
                            self.tiles[y][x] = 0  # Пол

    def draw(self, screen):
        # Отрисовка уровня
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(screen, (128, 128, 128), (x * 40, y * 40, 40, 40))