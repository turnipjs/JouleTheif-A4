import pygame
import game
import level_test
import sys

SIZE = (1700,900)

pygame.init()
game = game.JouleThiefGame(pygame.display.set_mode(SIZE, pygame.FULLSCREEN if "fullscreen" in sys.argv else 0))
game.set_state(level_test.LevelExample()).mainloop()
