import heapq
from typing import List, Tuple, Dict

SCREEN_SIZE = (1500, 1000)


import heapq
from typing import List, Tuple, Dict

class Pathfinder:
    def __init__(self, walls, grid_size=50):
        self.grid_size = grid_size
        self.obstacles = self._preprocess_obstacles(walls)
        
    def _preprocess_obstacles(self, walls):
        #Создаем множество с координатами всех непроходимых клеток"""
        obstacles = set()
        for wall in walls:
            if wall.typew not in not_col:  # Только непроходимые стены
                # Преобразуем границы стены в клетки сетки
                left = wall.rect.left // self.grid_size
                right = (wall.rect.right - 1) // self.grid_size
                top = wall.rect.top // self.grid_size
                bottom = (wall.rect.bottom - 1) // self.grid_size
                
                for x in range(left, right + 1):
                    for y in range(top, bottom + 1):
                        obstacles.add((x, y))
        return obstacles

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        #Оптимизированный A* с кешированием"""
        start_node = (start[0] // self.grid_size, start[1] // self.grid_size)
        end_node = (end[0] // self.grid_size, end[1] // self.grid_size)

        if end_node in self.obstacles:
            return []

        open_set = []
        heapq.heappush(open_set, (0, start_node))
        came_from = {}
        g_score = {start_node: 0}
        f_score = {start_node: self._heuristic(start_node, end_node)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end_node:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, end_node)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def _heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, node):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        for dx, dy in directions:
            neighbor = (node[0] + dx, node[1] + dy)
            if neighbor not in self.obstacles:
                neighbors.append(neighbor)
        return neighbors