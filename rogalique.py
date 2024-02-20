import random

def find_empty(map_grid, empty_symb):
    foundempty = False
    while (foundempty == False):
        x = random.randint(0, len(map_grid)-1)
        y = random.randint(0, len(map_grid[0])-1)
        foundempty = (map_grid[x][y] == empty_symb)
    return x, y

def place_at_empty(subj, map_grid, num=1):
    for _ in range(num):
        x_empty, y_empty = find_empty(map_grid, ' ')
        map_grid[x_empty][y_empty] = subj
    return map_grid

# Размеры карты
map_width = 40
map_height = 24

# Создание карты, заполненной стенами
map_grid = [['#'] * map_width for _ in range(map_height)]

# Комнаты
rooms_number = random.randint(5, 10)
room_minsize = 3
room_maxsize = 8
print("rooms_number = ", rooms_number)

# генерация комнат
for room in range(1, rooms_number+1):
    room_x = random.randint(1, map_width)
    room_y = random.randint(1, map_height)
    room_width = random.randint(room_minsize, room_maxsize)
    if ((map_width-room_x) < room_width):
        room_width = map_width-room_x
    room_height = random.randint(room_minsize, room_maxsize)
    if ((map_height-room_y) < room_height):
        room_height = map_height-room_y
    
    for height in range(room_height):
        for width in range(room_width):
            map_grid[room_y+height-1][room_x+width-1] = ' '

# генерация линий
# to do:
# обеспечить доступность каждой комнаты
# линии не должны оказаться друг в друге - в функцию подавать уже занятые места
# линии не должны быть рядом (ширина прохода 1 блок)
horizontal_lines_number = random.randint(3, 5)
print("horiz = ", horizontal_lines_number)
vertical_lines_number = random.randint(3, 5)
print("vert = ", vertical_lines_number)

for _ in range(horizontal_lines_number):
    map_grid[random.randint(1, map_height)-1] = [' ']*map_width

for _ in range(vertical_lines_number):
    col = random.randint(1, map_width)
    for row in map_grid:
        row[col-1] = ' '

# генерация мечей и зелий
# to do:
# не должны оказаться друг в друге - в функцию подавать уже занятые места
swords_num = 2
poison_num = 10
map_grid = place_at_empty('T', map_grid, swords_num)
map_grid = place_at_empty('Q', map_grid, poison_num)

# Вывод карты для проверки
for row in map_grid:
    print(''.join(row))
