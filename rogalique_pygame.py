import pygame, sys
from settings import *
from level import *

# Pygame setup
pygame.init()
pygame.mixer.init() #звук
screen = pygame.display.set_mode((map_width*tilesize, map_height*tilesize))
clock = pygame.time.Clock()  # to control frames per second

# основной цикл игры
if __name__ == '__main__':
    level = Level(generate_level(), screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Обработка нажатия клавиш
                if event.key == pygame.K_LEFT:
                    level.player.sprite.move(-1, 0, level)  # Передвижение игрока влево
                elif event.key == pygame.K_RIGHT:
                    level.player.sprite.move(1, 0, level)  # Передвижение игрока вправо
                elif event.key == pygame.K_UP:
                    level.player.sprite.move(0, -1, level)  # Передвижение игрока вверх
                elif event.key == pygame.K_DOWN:
                    level.player.sprite.move(0, 1, level)  # Передвижение игрока вниз

        # background
        screen.fill('black')
        # draw a level
        level.draw_tiles()
        pygame.display.update()
        screen.blit(level.player.sprite.image, level.player.sprite.rect)
        clock.tick(FPS)  # set fps


'''
для каждой комнаты  есть  ли  строка, в которой все иксы?

комнаты не пересек
при генерации комнат хотя бы 1 символ уже пустота - перегенерация комнаты

потом генерация  линий
хотя бы 1 символ не пришлось заменять - 1 пересечение
'''