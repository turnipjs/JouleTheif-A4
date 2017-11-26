import pygame
import game
import level_test

SIZE = (1700,900)

pygame.init()
game = game.JouleThiefGame(pygame.display.set_mode(SIZE))
game.set_state(level_test.LevelExample()).mainloop()