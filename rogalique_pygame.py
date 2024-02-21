import pygame, sys
from settings import *
from level import *

# Pygame setup
pygame.init()
pygame.mixer.init() #звук
screen = pygame.display.set_mode((map_width*tilesize, map_height*tilesize))
clock = pygame.time.Clock()  # to control frames per second

level = Level(generate_level(), screen)

# основной цикл игры
if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # background
        screen.fill('black')
        # draw a level
        level.draw_tiles()

        pygame.display.update()
        clock.tick(FPS)  # set fps

# Вывод карты для проверки
for row in map_grid:
    print(''.join(row))
