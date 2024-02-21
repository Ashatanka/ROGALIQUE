from settings import *
import random
import pygame

def find_empty(map_grid, empty_symb):
    foundempty = False
    while (foundempty == False):
        x = random.randint(0, len(map_grid)-1)
        y = random.randint(0, len(map_grid[0])-1)
        foundempty = (map_grid[x][y] == empty_symb)
    return x, y

def place_at_empty(subj, map_grid, empty_symb, num=1):
    for _ in range(num):
        x_empty, y_empty = find_empty(map_grid, empty_symb)
        map_grid[x_empty][y_empty] = subj
    return map_grid

def room_generate(map_grid):

    def room_settings():
        room_x = random.randint(1, map_width) # столбец
        room_y = random.randint(1, map_height) # строка
        room_width = random.randint(room_minsize, room_maxsize) #6
        if ((map_width-room_x+1) < room_width):
            room_width = map_width-room_x+1
        room_height = random.randint(room_minsize, room_maxsize) #3
        if ((map_height-room_y+1) < room_height):
            room_height = map_height-room_y+1
        return room_x, room_y, room_width, room_height

    def place_room(map):
        cash = [row[:] for row in map]
        r_x, r_y, r_width, r_height = room_settings()
        print("r_x, r_y, r_width, r_height = ", r_x, r_y, r_width, r_height)
        for height in range(r_height):
                for width in range(r_width):
                    if map[r_y+height-1][r_x+width-1] == empty_symb:
                        print("overlay!")
                        map = [i[:] for i in cash]
                        for ind_row, row in enumerate(map):
                            print(''.join(row), ind_row)
                        return place_room(map)
                    else:
                        map[r_y+height-1][r_x+width-1] = empty_symb
        return map

    return place_room(map_grid)
    '''# place room on map
    cash = map_grid
    no_overlay = True
    r_x, r_y, r_width, r_height = room_settings()
    print("r_x, r_y, r_width, r_height = ", r_x, r_y, r_width, r_height)
    for height in range(r_height):
            for width in range(r_width):
                if map_grid[r_y+height-1][r_x+width-1] == empty_symb:
                    no_overlay = False
                    print("overlay!")
                    break
                else:
                    map_grid[r_y+height-1][r_x+width-1] = empty_symb
            print(no_overlay, "ok!")
    if no_overlay:
        return map_grid
    else:
        map_grid = cash
        return room_generate(map_grid)'''

def generate_level():
    # Создание карты, заполненной стенами
    map_grid = [[wall_symb] * map_width for _ in range(map_height)]

    # Генерация комнат
    rooms_number = random.randint(room_minnum, room_maxnum)
    print("rooms_number = ", rooms_number)

    for room in range(1, rooms_number+1):
        map_grid = room_generate(map_grid)
        print('NEW ROOM')
        for ind_row, row in enumerate(map_grid):
            print(''.join(row), ind_row)

    for row in map_grid:
        print(''.join(row))
    # генерация линий
    # to do:
    # обеспечить доступность каждой комнаты
    # линии не должны оказаться друг в друге - в функцию подавать уже занятые места
    # линии не должны быть рядом (ширина прохода 1 блок)
    horizontal_lines_number = random.randint(lines_minnumber, lines_maxnumber)
    vertical_lines_number = random.randint(lines_minnumber, lines_maxnumber)
    print("horiz = ", horizontal_lines_number)
    print("vert = ", vertical_lines_number)

    for _ in range(horizontal_lines_number):
        map_grid[random.randint(1, map_height)-1] = [empty_symb]*map_width

    for _ in range(vertical_lines_number):
        col = random.randint(1, map_width)
        for row in map_grid:
            row[col-1] = empty_symb

    # генерация мечей и зелий
    # to do:
    # не должны оказаться друг в друге - в функцию подавать уже занятые места
    map_grid = place_at_empty(sword_symb, map_grid, empty_symb, swords_num)
    map_grid = place_at_empty(poison_symb, map_grid, empty_symb, poison_num)

    # генерация героя
    hero_x, hero_y = find_empty(map_grid, empty_symb)
    map_grid[hero_x][hero_y] = hero_symb

    # субъекты класса противников
    # ...
    return map_grid

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, cell):
        super().__init__()
        #self.image = pygame.Surface((size, size))
        #self.image.fill('grey')
        if cell == empty_symb:
            self.image = pygame.image.load('src\/tile-.png')
        else:
            self.image = pygame.image.load('src\/tile-W.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('src\/tile-P.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('src\/tile-E.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

class Sword(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('src\/tile-SW.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

class Poison(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('src\/tile-HP.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)
class Level:
    def __init__(self, map_grid, screen):
        self.display_surface = screen # экран как свойство уровня
        self.setup_level(map_grid) # при инициализации создаём плитки

    def setup_level(self, map_grid):
        # уровень включает в себя плитки, игрока, предметы и врагов
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # создаем  плитки согласно карте
        for row_index, row in enumerate(map_grid):
            for col_index, cell in enumerate(row):
                x = col_index * tilesize
                y = row_index * tilesize

                if cell == wall_symb or cell == empty_symb:
                    tile = Tile((x, y), tilesize, cell)
                    self.tiles.add(tile)
                elif cell == hero_symb:
                    player_sprite = Player((x, y), tilesize)
                    self.player.add(player_sprite)
                elif cell == sword_symb:
                    sword_sprite = Sword((x, y), tilesize)
                    self.items.add(sword_sprite)
                elif cell == poison_symb:
                    poison_sprite = Poison((x, y), tilesize)
                    self.items.add(poison_sprite)


    # рисуем созданные плитки
    def draw_tiles(self):
        # level tiles
        self.tiles.update()
        self.tiles.draw(self.display_surface)

        # player
        self.player.draw(self.display_surface)

        self.items.draw(self.display_surface)         