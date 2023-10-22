import random
import pygame as pg
from cell import Cell
import smart_rect


class Area:
    def __init__(self, owner, addresses):
        settings = open("settings.txt", "r")
        mode, num_mines, width, height = settings.read().split("\n")
        settings.close()
        self.width = int(width)
        self.height = int(height)
        self.num_mines = int(num_mines)
        self.cell_width = 40
        self.width_px = self.width * self.cell_width
        self.height_px = self.height * self.cell_width
        self.owner = owner
        self.address = addresses
        self.address["area"] = self
        self.root = pg.Surface((self.width_px, self.height_px))
        '''Шпора по индексам спрайтов : 0 - пустота, 1-8 - номера, 9 - мина, 10 - крышка, 11 - флаг'''
        self.sprites = [pg.image.load("sapper_sprites/space.png"), pg.image.load("sapper_sprites/n1.png"),
                        pg.image.load("sapper_sprites/n2.png"), pg.image.load("sapper_sprites/n3.png"),
                        pg.image.load("sapper_sprites/n4.png"), pg.image.load("sapper_sprites/n5.png"),
                        pg.image.load("sapper_sprites/n6.png"), pg.image.load("sapper_sprites/n7.png"),
                        pg.image.load("sapper_sprites/n8.png"), pg.image.load("sapper_sprites/mina.png"),
                        pg.image.load("sapper_sprites/lid.png"), pg.image.load('sapper_sprites/flag.png')]
        self.rect = pg.rect.Rect(0, 0, 620, 620)
        self.MAP = [[Cell((y, x), self) for x in range(self.width)] for y in range(self.height)]
        self.smart_rect = smart_rect.SmartRect(self.root, (self.rect.w, self.rect.h))
        self.init_map()

    def new_game(self):
        self.init_map()
        self.address["panel"].game_stat = 2
        self.address["panel"].timer_on = True
        self.smart_rect = smart_rect.SmartRect(self.root, (self.rect.w, self.rect.h))

    def init_map(self):
        for line in self.MAP:
            for cell in line:
                cell.num = 0
                cell.lid = "#"
        mines_count = self.num_mines
        while mines_count != 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.MAP[y][x].num != 9:
                self.MAP[y][x].become_mine()
                mines_count -= 1
        for line in self.MAP:
            for cell in line:
                cell.draw()

    def check_on_finish(self):
        for line in self.MAP:
            for cell in line:
                if cell.num != 9 and cell.lid != "*":
                    return False
        return True

    def stop_game(self, stat):
        if stat == "def":
            for line in self.MAP:
                for cell in line:
                    cell.lid = "*"
                    cell.draw()
        self.address["panel"].stop_game(stat)

    def set_motion(self, xy, vec):
        if pg.mouse.get_pressed()[0]:
            self.smart_rect.move(vec)

    def set_click(self, xy, btn):
        if btn == 1 or btn == 3:
            xy = self.smart_rect.get_absolut_xy(xy)
            x = xy[0] // self.cell_width
            y = xy[1] // self.cell_width
            self.MAP[y][x].you_clicking(btn)

    def set_down(self, xy, btn):
        self.smart_rect.get_scale(btn)

    def draw(self):
        self.owner.blit(self.smart_rect.get_image(), (0, 0))

    def get_rect(self):
        return self.rect



