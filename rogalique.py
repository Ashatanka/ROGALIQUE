import random

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
    room_width = random.randint(room_minsize, room_maxsize) #4
    if ((map_width-room_x) < room_width):
        room_width = map_width-room_x
    room_height = random.randint(room_minsize, room_maxsize)
    if ((map_height-room_y) < room_height):
        room_height = map_height-room_y
    
    for height in range(room_height):
        for width in range(room_width):
            map_grid[room_y+height-1][room_x+width-1] = ' '

# Вывод карты для проверки
for row in map_grid:
    print(''.join(row))