import random
import pygame as pg

pg.init()

clock = pg.time.Clock()  # Таймер смены кадров
num_mines = 30           # Количество мин на поле, переменная используется для подсчёта уже расставленных мин
cell_width = 40          # Ширина одной клетки
map_width = 20           # Ширина карты в клетках
map_height = 20          # Высота карты в клетках
root_width = 620         # Ширина окна
root_height = 620        # Высота окна
perm_bias = (root_width - map_width * cell_width, root_height - map_height * cell_width)  # Максимальное доп. смещение

root = pg.display.set_mode((root_width, root_height))

'''Шпора по индексам спрайтов : 0 - пустота, 1-8 - номера, 9 - мина, 10 - крышка, 11 - флаг'''
sprites = [pg.image.load("sapper_sprites/space.png"), pg.image.load("sapper_sprites/n1.png"),
           pg.image.load("sapper_sprites/n2.png"), pg.image.load("sapper_sprites/n3.png"),
           pg.image.load("sapper_sprites/n4.png"), pg.image.load("sapper_sprites/n5.png"),
           pg.image.load("sapper_sprites/n6.png"), pg.image.load("sapper_sprites/n7.png"),
           pg.image.load("sapper_sprites/n8.png"), pg.image.load("sapper_sprites/mina.png"),
           pg.image.load("sapper_sprites/lid.png"), pg.image.load('sapper_sprites/flag.png')]


class Cell:
    global cell_width

    '''pos - позиция клетки на поле, owner - владелец клетки (нужен для вычисления относительного положения), 
    num - значение клетки (кол-во мин вокруг), lid - состояние крышки (close - закрыта, open - открыта, 
    flag - стоит флаг), pos_px - относительная позиция в окне'''

    def __init__(self, pos, owner, num):
        self.pos = pos
        self.owner = owner
        self.num = num
        self.lid = "close"
        self.pos_px = (self.pos[0] * cell_width + self.owner.pos[0],
                       self.pos[1] * cell_width + self.owner.pos[1])

    def draw(self):
        self.pos_px = (self.pos[0] * cell_width + self.owner.pos[0],
                       self.pos[1] * cell_width + self.owner.pos[1])
        if self.lid == "open":
            root.blit(sprites[self.num], (self.pos_px[0], self.pos_px[1]))
        else:
            if self.lid == "close":
                root.blit(sprites[10], (self.pos_px[0], self.pos_px[1]))
            else:
                root.blit(sprites[11], (self.pos_px[0], self.pos_px[1]))

    def click_on_me(self, btn):
        mouse_pos = pg.mouse.get_pos()

        if (mouse_pos[0] > self.pos_px[0]) and (mouse_pos[0] < self.pos_px[0] + cell_width) and (mouse_pos[1] > self.pos_px[1]) and (mouse_pos[1] < self.pos_px[1] + cell_width):
            if btn == 0:
                if self.lid == "flag":
                    self.lid = "close"
                else:
                    self.lid = "open"
                    self.owner.clean(self)
            else:
                self.lid = "flag"


class Area:
    def __init__(self, pos):
        self.pos = pos
        self.pos_2 = (pos[0] + map_width * cell_width, pos[1] + map_height * cell_width)
        self.MAP = []

    def init_map(self, owner):
        self.MAP = [[Cell((x, y), owner, 0) for x in range(map_width)] for y in range(map_height)]
        print(self.MAP[2][1].pos)

    def fill_map(self, mines_count):
        def check_on_mine(x, y):
            if (x < 0) or (x >= map_width) or (y < 0) or (y >= map_height):
                return 0
            else:
                if self.MAP[y][x].num == 9:
                    return 1
                return 0
        while mines_count != 0:
            x = random.randint(0, map_width - 1)
            y = random.randint(0, map_height - 1)
            if self.MAP[y][x].num != 9:
                self.MAP[y][x].num = 9
                mines_count -= 1
        for line in self.MAP:
            for cell in line:
                if cell.num != 9:
                    mines_count_count = 0
                    x, y = cell.pos[0], cell.pos[1]
                    mines_count_count += check_on_mine(x - 1, y - 1)
                    mines_count_count += check_on_mine(x, y - 1)
                    mines_count_count += check_on_mine(x + 1, y - 1)
                    mines_count_count += check_on_mine(x - 1, y)
                    mines_count_count += check_on_mine(x + 1, y)
                    mines_count_count += check_on_mine(x - 1, y + 1)
                    mines_count_count += check_on_mine(x, y + 1)
                    mines_count_count += check_on_mine(x + 1, y + 1)
                    cell.num = mines_count_count

    def get_position(self, x, y):
        def sum_bord(sum, bord):
            c = sum[0] + sum[1]
            if (c > bord[0]) and (c < bord[1]):
                return c
            elif c <= bord[0]:
                return bord[0]
            else:
                return bord[1]

        if perm_bias[0] < 0:
            self.pos = (sum_bord((self.pos[0], x), (perm_bias[0], 0)), self.pos[1])
        if perm_bias[1] < 0:
            self.pos = (self.pos[0], sum_bord((self.pos[1], y), (perm_bias[1], 0)))

    def clean(self, cell):
        if cell.num == 0:
            y, x = cell.pos[1], cell.pos[0]
            cells = [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]
            while len(cells) != 0:
                for num in cells:
                    y, x = num[0], num[1]
                    if (y < 0) or (y >= map_height) or (x < 0) or (x >= map_width):
                        break
                    cell = self.MAP[y][x]
                    cells.remove(num)
                    if cell.num != 9 and cell.lid != "open":
                        cell.lid = "open"
                        if cell.num == 0:
                            cells.append((cell.pos[1], cell.pos[0] - 1))
                            cells.append((cell.pos[1], cell.pos[0] + 1))
                            cells.append((cell.pos[1] - 1, cell.pos[0]))
                            cells.append((cell.pos[1] + 1, cell.pos[0]))
                    self.MAP[y][x] = cell


class Click_Manager():
    def __init__(self, func, btn):
        self.click = False
        self.up = False
        self.past = None
        self.func = func
        self.past_pos = None
        self.btn = btn

    def get_click(self):
        def roughly_equal(p1, p2):
            n = 10
            if (p1[0] - n > p2[0]) or (p1[0] + n < p2[0]) or (p1[1] + n < p2[1]) or (p1[1] + n < p2[1]):
                return False
            return True

        pres = pg.mouse.get_pressed()
        if pres[self.btn] and not self.past:
            self.click = True
            self.past = True
            self.past_pos = pg.mouse.get_pos()
        elif not pres[self.btn] and self.past:
            self.up = True
            self.past = False
        if self.click and self.up:
            if roughly_equal(self.past_pos, pg.mouse.get_pos()):
                self.func(self.btn)
            self.click, self.up = False, False


def draw_all():
    for line in area.MAP:
        for cell in line:
            cell.draw()


def check_click(btn):
    for line in area.MAP:
        for cell in line:
            cell.click_on_me(btn)


area = Area((0, 0))
area.init_map(area)
area.fill_map(num_mines)

click_right = Click_Manager(check_click, 0)
click_left = Click_Manager(check_click, 2)

past_pos = pg.mouse.get_pos()
run = True
while run:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEMOTION:
            click = pg.mouse.get_pressed()
            new_pos = pg.mouse.get_pos()
            if click[0]:
                area.get_position(new_pos[0] - past_pos[0], new_pos[1] - past_pos[1])
            past_pos = new_pos

    click_right.get_click()
    click_left.get_click()
    draw_all()
    pg.display.update()
pg.quit()




