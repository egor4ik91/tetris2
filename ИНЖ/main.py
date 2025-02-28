import pygame
import sys
from game import TetrisGame

def main():
    pygame.init()
    pygame.font.init()
    game = TetrisGame()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()