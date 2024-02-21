import pygame, sys
from settings import *
from level import *

# Pygame setup
pygame.init()
tilesize = 24
screen = pygame.display.set_mode((map_width*tilesize, map_height*tilesize))
clock = pygame.time.Clock()  # to control frames per second


print("rooms_number = ", rooms_number)
print("horiz = ", horizontal_lines_number)
print("vert = ", vertical_lines_number)

# основной цикл игры
if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # background
        screen.fill('black')
        # ... draw a level

        pygame.display.update()
        clock.tick(60)  # set fps

# Вывод карты для проверки
for row in map_grid:
    print(''.join(row))
