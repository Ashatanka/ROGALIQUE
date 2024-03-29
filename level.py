from settings import *
import random
import pygame, sys
import tkinter as tk

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

def check_near(r_x, r_y, r_width, r_height, map_grid):
        # note that r_x and r_y are from 0
        if r_x != 0: # left
            for i in range(r_y - (r_y != 0), r_y + r_height + (r_y + r_height != map_height)):
                if map_grid[i][r_x-1] == empty_symb: return False
        if r_x + r_width != map_width: # right
            for i in range(r_y - (r_y != 0), r_y + r_height + (r_y + r_height != map_height)):
                if map_grid[i][r_x + r_width] == empty_symb: return False
        if r_y != 0: # up
            for i in range(r_x, r_x+r_width):
                if map_grid[r_y-1][i] == empty_symb: return False
        if r_y + r_height != map_height:
            for i in range(r_x, r_x+r_width):
                if map_grid[r_y + r_height][i] == empty_symb: return False
        return True

def room_generate(map_grid, roomslist):

    def room_settings():
        room_x = random.randint(0, map_width-1) # столбец
        room_y = random.randint(0, map_height-1) # строка
        room_width = random.randint(room_minsize, room_maxsize) #6
        if ((map_width-room_x) < room_width):
            room_width = map_width-room_x
        room_height = random.randint(room_minsize, room_maxsize) #3
        if ((map_height-room_y) < room_height):
            room_height = map_height-room_y
        return room_x, room_y, room_width, room_height

    def place_room(map, rooms):
        # cash = [row[:] for row in map]
        r_x, r_y, r_width, r_height = room_settings()
        if not check_near(r_x, r_y, r_width, r_height, map):
            return place_room(map, rooms)
        for height in range(r_height):
                for width in range(r_width):
                    map[r_y+height][r_x+width] = empty_symb
        rooms.append({'r_x': r_x, 'r_y': r_y, 'r_width': r_width, 'r_height': r_height})
        return map, rooms

    return place_room(map_grid, roomslist)

def generate_level():
    # Создание карты, заполненной стенами
    map_grid = [[wall_symb] * map_width for _ in range(map_height)]

    # Генерация комнат
    rooms_number = random.randint(room_minnum, room_maxnum)
    roomslist = []
    for room in range(1, rooms_number+1):
        map_grid, roomslist = room_generate(map_grid, roomslist)

    # генерация линий
    # to do:
    # обеспечить доступность каждой комнаты
    # линии не должны оказаться друг в друге - в функцию подавать уже занятые места
    # линии не должны быть рядом (ширина прохода 1 блок)
    horizontal_lines_number = random.randint(lines_minnumber, lines_maxnumber)
    vertical_lines_number = random.randint(lines_minnumber, lines_maxnumber)

    for i in range(rooms_number):
        if check_near(*(roomslist[i].values()), map_grid):
            if horizontal_lines_number != 0:
                line_y = random.randint(roomslist[i]["r_y"], roomslist[i]["r_y"] + roomslist[i]["r_height"] - 1)
                map_grid[line_y] = [empty_symb]*map_width
                horizontal_lines_number -= 1
            elif vertical_lines_number != 0:
                line_x = random.randint(roomslist[i]["r_x"], roomslist[i]["r_x"] + roomslist[i]["r_width"] - 1)
                for row in map_grid:
                    row[line_x] = empty_symb
                vertical_lines_number -= 1
    
    while horizontal_lines_number != 0:
        line_y = random.randint(0, map_height-1)
        map_grid[line_y] = [empty_symb]*map_width
        horizontal_lines_number -= 1

    while vertical_lines_number != 0:
        line_x = random.randint(0, map_width-1)
        for row in map_grid:
            row[line_x] = empty_symb
        vertical_lines_number -= 1
            

    # генерация мечей и зелий
    # to do:
    # не должны оказаться друг в друге - в функцию подавать уже занятые места
    map_grid = place_at_empty(sword_symb, map_grid, empty_symb, swords_num)
    map_grid = place_at_empty(poison_symb, map_grid, empty_symb, poison_num)

    # генерация героя
    hero_x, hero_y = find_empty(map_grid, empty_symb)
    map_grid[hero_x][hero_y] = hero_symb

    # противников
    map_grid = place_at_empty(enemy_symb, map_grid, empty_symb, enemies_num)

    return map_grid

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, cell):
        super().__init__()
        self.tiletype = 'other'
        #self.image = pygame.Surface((size, size))
        #self.image.fill('grey')
        if cell == wall_symb:
            self.image = pygame.image.load('src\/tile-W.png')
            self.tiletype = 'wall'
        else:
            self.image = pygame.image.load('src\/tile-.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('src\/tile-P.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pos
        self.hp = 10
        self.strength = 1

    def move(self, dx, dy, level):
        new_pos = (self.pos[0] + dx * tilesize, self.pos[1] + dy * tilesize)
        if 0 <= new_pos[0] < map_width * tilesize and 0 <= new_pos[1] < map_height * tilesize:
            
            new_rect = pygame.Rect(new_pos[0], new_pos[1], self.rect.width, self.rect.height)
            
            for tile in level.tiles:
                if tile.tiletype == 'wall' and tile.rect.colliderect(new_rect):
                    # Если есть стена на новой позиции, игрок не может сделать этот шаг
                    return
            for enemy in level.enemies:
                if enemy.rect.colliderect(new_rect):
                    self.hp -= 1
                    return
                
            for item in level.items:
                if item.tiletype == 'poison' and item.rect.colliderect(new_rect):
                    self.hp += 1
                    item.kill()
                elif item.tiletype == 'sword' and item.rect.colliderect(new_rect):
                    self.strength += 1
                    item.kill()
            
            # Если нет стены на пути, обновляем позицию игрока
            self.pos = new_pos
            self.rect = new_rect
        
    def attack(self, level):
        for enemy in level.enemies:
            enemy_x, enemy_y = enemy.rect.topleft
            if (enemy_x - self.pos[0] in [-tilesize, tilesize] and enemy_y == self.pos[1]) or \
                        (enemy_y - self.pos[1] in [-tilesize, tilesize] and enemy_x == self.pos[0]):
                enemy.hp -= self.strength
                if enemy.hp <= 0:
                    enemy.kill()
        return

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load('src\/tile-E.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pos
        self.hp = 10

    def move(self, level):
        variety = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = variety[random.randint(0, len(variety) - 1)]
        new_pos = (self.pos[0] + dx * tilesize, self.pos[1] + dy * tilesize)
        if 0 <= new_pos[0] < map_width * tilesize and 0 <= new_pos[1] < map_height * tilesize:
            
            new_rect = pygame.Rect(new_pos[0], new_pos[1], self.rect.width, self.rect.height)
            
            for tile in level.tiles:
                if tile.tiletype == 'wall' and tile.rect.colliderect(new_rect):
                    # Если есть стена на новой позиции, игрок не может сделать этот шаг
                    return
            for player in level.player:
                if player.rect.colliderect(new_rect):
                    player.hp -= 1
                    return
            
            # Если нет стены на пути, обновляем позицию игрока
            self.pos = new_pos
            self.rect = new_rect

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, size, cell):
        super().__init__()
        self.tiletype = 'other'
        if cell == sword_symb:
            self.image = pygame.image.load('src\/tile-SW.png')
            self.tiletype = 'sword'
        elif cell == poison_symb:
            self.image = pygame.image.load('src\/tile-HP.png')
            self.tiletype = 'poison'
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = pos)
        
class Level:
    def __init__(self, map_grid, screen):
        self.display_surface = screen # экран как свойство уровня
        self.setup_level(map_grid) # при инициализации создаём плитки
        self.font = pygame.font.Font(None, 36)  # Создаем объект шрифта для отображения текста

    def setup_level(self, map_grid):
        # уровень включает в себя плитки, игрока, предметы и врагов
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # создаем плитки согласно карте
        for row_index, row in enumerate(map_grid):
            for col_index, cell in enumerate(row):
                x = col_index * tilesize
                y = row_index * tilesize

                tile = Tile((x, y), tilesize, cell)
                self.tiles.add(tile)
                if cell == hero_symb:
                    player_sprite = Player((x, y), tilesize)
                    self.player.add(player_sprite)
                elif cell == enemy_symb:
                    enemy_sprite = Enemy((x, y), tilesize)
                    self.enemies.add(enemy_sprite)
                elif cell == sword_symb:
                    sword_sprite = Item((x, y), tilesize, cell)
                    self.items.add(sword_sprite)
                elif cell == poison_symb:
                    poison_sprite = Item((x, y), tilesize, cell)
                    self.items.add(poison_sprite)

    def draw_health(self, player, enemies):
        for enemy in self.enemies:
            # Создаем текстовый объект, отображающий здоровье игрока
            health_text = self.font.render(f'HP: {enemy.hp}', True, (255, 255, 255))
            # Получаем прямоугольник, ограничивающий текстовый объект
            text_rect = health_text.get_rect()
            # Помещаем прямоугольник над игроком
            text_rect.center = (enemy.rect.centerx, enemy.rect.centery - 20)
            # Отображаем текстовый объект на экране
            self.display_surface.blit(health_text, text_rect)
        # Создаем текстовый объект, отображающий здоровье игрока
        health_text = self.font.render(f'HP: {player.hp}', True, (255, 255, 255))
        # Получаем прямоугольник, ограничивающий текстовый объект
        text_rect = health_text.get_rect()
        # Помещаем прямоугольник над игроком
        text_rect.center = (player.rect.centerx, player.rect.centery - 20)
        # Отображаем текстовый объект на экране
        self.display_surface.blit(health_text, text_rect)

    # рисуем созданные плитки
    def draw_tiles(self):
        # level tiles
        self.tiles.update()
        self.tiles.draw(self.display_surface)

        # player
        self.player.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.items.draw(self.display_surface)
        self.draw_health(self.player.sprite, self.enemies.sprites)         

    def game_over(self):
        # Создаем окно
        game_over_window = tk.Tk()
        game_over_window.title("Game Over")

        # Создаем текстовое сообщение
        label = tk.Label(game_over_window, text="Game Over", font=("Helvetica", 24))
        label.pack(pady=20)

        def play_again():
            game_over_window.destroy()  # Закрываем окно
        
        def close():
            game_over_window.destroy()  # Закрываем окно
            pygame.quit()  # Завершаем Pygame
            sys.exit()  # Завершаем программу

        # Создаем кнопки
        button_play_again = tk.Button(game_over_window, text="Играть ещё", command=play_again)
        button_play_again.pack(side=tk.LEFT, padx=10)
        button_close = tk.Button(game_over_window, text="Закрыть", command=close)
        button_close.pack(side=tk.RIGHT, padx=10)

        game_over_window.mainloop()  # Запускаем главный цикл tkinter
