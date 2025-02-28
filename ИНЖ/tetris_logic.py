import pygame
import random

class TetrisLogic:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid = [[0] * grid_width for _ in range(grid_height)]
        self.current_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        shapes = [
            [[1, 1, 1, 1]],  # I
            [[2, 0, 0], [2, 2, 2]],  # J
            [[0, 0, 3], [3, 3, 3]],  # L
            [[4, 4], [4, 4]],  # O
            [[0, 5, 5], [5, 5, 0]],  # S
            [[0, 6, 0], [6, 6, 6]],  # T
            [[7, 7, 0], [0, 7, 7]]  # Z
        ]
        shape = random.choice(shapes)
        return {
            'shape': shape,
            'x': self.grid_width // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def move(self, dx, dy):
        if self.valid_move(dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
        elif dy > 0:  # Если движение вниз невозможно
            self.merge_piece()
            self.current_piece = self.new_piece()
            if not self.valid_move(0, 0):
                self.game_over = True

    def valid_move(self, dx, dy):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_piece['x'] + j + dx
                    y = self.current_piece['y'] + i + dy
                    if x < 0 or x >= self.grid_width or y >= self.grid_height or (y >= 0 and self.grid[y][x]):
                        return False
        return True

    def rotate(self):
        rotated_shape = list(zip(*reversed(self.current_piece['shape'])))  # Вращение фигуры
        original_shape = self.current_piece['shape']  # Сохраняем оригинальную фигуру
        self.current_piece['shape'] = rotated_shape  # Применяем вращение

        # Проверка на допустимость вращения
        if not self.valid_move(0, 0):
            self.current_piece['shape'] = original_shape  # Если недопустимо, возвращаем оригинал

    def merge_piece(self):
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = cell

    def clear_lines(self):
        lines_cleared = 0
        for i in range(self.grid_height):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0] * self.grid_width)
                lines_cleared += 1
        return lines_cleared

    def update(self):
        if self.valid_move(0, 1):
            self.move(0, 1)  # Движение вниз
            return False
        return True

    def draw(self, screen):
        # Рисуем сетку
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                pygame.draw.rect(screen, (50, 50, 50), (j * 30, i * 30, 29, 29), 1)  # Рисуем линии сетки

        # Рисуем заполненные клетки
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 255, 255), (j * 30, i * 30, 29, 29))

        # Рисуем текущую фигуру
        for i, row in enumerate(self.current_piece['shape']):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 0, 0), ((self.current_piece['x'] + j) * 30,
                                                           (self.current_piece['y'] + i) * 30, 29, 29))