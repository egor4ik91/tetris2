import pygame
import random
from database import DatabaseManager
from tetris_logic import TetrisLogic


class TetrisGame:
    def __init__(self):
        self.width = 300
        self.height = 600
        self.block_size = 30
        self.grid_width = 10
        self.grid_height = 20

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tetris")

        self.db = DatabaseManager()
        self.font = pygame.font.SysFont(None, 36)

        self.username = self.get_username()
        self.init_game()

    def get_username(self):
        username = ""
        input_active = True

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and username:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 10:
                            username += event.unicode

            self.screen.fill((0, 0, 0))
            text_surface = self.font.render(f"Введите имя: {username}", True, (255, 255, 255))
            self.screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height // 2))
            pygame.display.flip()

        return username

    def init_game(self):
        self.tetris = TetrisLogic(self.grid_width, self.grid_height)
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500  # Задержка в миллисекундах

    def run(self):
        while not self.tetris.game_over:
            current_time = pygame.time.get_ticks()
            if current_time - self.fall_time > self.fall_speed:
                self.tetris.move(0, 1)
                self.fall_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.tetris.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.tetris.move(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.tetris.move(1, 0)
                    if event.key == pygame.K_DOWN:
                        self.tetris.move(0, 1)
                    if event.key == pygame.K_UP:
                        self.tetris.rotate()  # Вращение фигуры

            if self.tetris.update():
                self.score += self.tetris.clear_lines() * 100

            self.draw()
            pygame.time.delay(100)

        self.end_game()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.tetris.draw(self.screen)
        score_text = self.font.render(f"Счет: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def end_game(self):
        self.db.save_score(self.username, self.score)
        top_scores = self.db.get_top_scores()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill((0, 0, 0))
            game_over_text = self.font.render('Игра окончена!', True, (255, 255, 255))
            self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 4))
            score_text = self.font.render(f'Ваш счет: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 3))

            title_text = self.font.render('Топ 5 игроков:', True, (255, 255, 255))
            self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 2 - 40))
            for i, (name, score) in enumerate(top_scores):
                score_line = self.font.render(f'{i + 1}. {name}: {score}', True, (255, 255, 255))
                self.screen.blit(score_line, (self.width // 2 - score_line.get_width() // 2, self.height // 2 + i * 30))

            pygame.display.flip()