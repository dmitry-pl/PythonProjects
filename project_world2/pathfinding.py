import heapq
from typing import List, Tuple, Dict

SCREEN_SIZE = (1500, 1000)


class Pathfinder:
    def __init__(self, walls, grid_size=50):
        self.grid_size = grid_size
        self.obstacle_grid = self._build_obstacle_grid(walls)
    
    def _build_obstacle_grid(self, walls) -> List[List[bool]]:
        grid_width = SCREEN_SIZE[0] // self.grid_size
        grid_height = SCREEN_SIZE[1] // self.grid_size
        grid = [[False for _ in range(grid_height)] for _ in range(grid_width)]
        
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
        start_node = self._world_to_grid(start)
        end_node = self._world_to_grid(end)
        
        if not self._valid_node(end_node):
            return []
        
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
        
        return []

    def _world_to_grid(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        return (pos[0] // self.grid_size, pos[1] // self.grid_size)

    def _valid_node(self, node: Tuple[int, int]) -> bool:
        x, y = node
        return (0 <= x < len(self.obstacle_grid) and 
                0 <= y < len(self.obstacle_grid[0]) and 
                not self.obstacle_grid[x][y])

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        
        for dx, dy in directions:
            neighbor = (node[0] + dx, node[1] + dy)
            if self._valid_node(neighbor):
                neighbors.append(neighbor)
                
        return neighbors

    def _reconstruct_path(self, came_from: Dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path