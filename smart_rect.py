import pygame as pg


class SmartRect:
    def __init__(self, main_image, transform_to):
        self.main_image = main_image
        self.transform_to = transform_to
        self.pos = [[0, 0], [400, 400]]
        self.scale = 0
        self.width = self.pos[1][0] - self.pos[0][0] + 1
        self.height = self.pos[1][1] - self.pos[0][1] + 1

    def get_image(self):
        x1, y1 = self.pos[0][0], self.pos[0][1]
        full_image = pg.Surface((self.width, self.height))
        full_image.blit(self.main_image, (0, 0), (x1, y1, self.width, self.height))
        return pg.transform.scale(full_image, self.transform_to)

    def align(self):
        if self.pos[0][0] < 0:
            self.pos[0][0] = 0
            self.pos[1][0] = self.width - 1
        if self.pos[0][1] < 0:
            self.pos[0][1] = 0
            self.pos[1][1] = self.height - 1
        if self.pos[1][0] >= self.main_image.get_width() - 1:
            self.pos[1][0] = self.main_image.get_width() - 1
            self.pos[0][0] = self.main_image.get_width() - self.width
        if self.pos[1][1] >= self.main_image.get_height() - 1:
            self.pos[1][1] = self.main_image.get_height() - 1
            self.pos[0][1] = self.main_image.get_height() - self.height

    def move(self, vec):
        vec = (round(vec[0] * (self.width / self.transform_to[0])),
               round(vec[1] * (self.width / self.transform_to[1])))
        pos = (self.pos[0][0] - vec[0], self.pos[0][1] - vec[1])
        self.pos[0][0] = pos[0]
        self.pos[0][1] = pos[1]
        self.pos[1][0] = pos[0] + self.width - 1
        self.pos[1][1] = pos[1] + self.height - 1
        self.align()

    def get_scale(self, btn):
        if btn == 5 and self.scale < 80:
            if self.main_image.get_width() <= self.width or self.main_image.get_height() <= self.height:
                return None
            self.scale += 1
            growth = 10
        elif btn == 4 and self.scale > -18:
            self.scale -= 1
            growth = -10
        else:
            return None

        new_w = self.width + growth
        new_h = self.height + growth
        if new_w > self.main_image.get_width():
            new_w = self.main_image.get_width()
        if new_h > self.main_image.get_height():
            new_h = self.main_image.get_height()
            new_w = new_h

        self.pos[1][0] = self.pos[0][0] + new_w - 1
        self.pos[1][1] = self.pos[0][1] + new_h - 1
        half = growth / 2
        self.pos[0][0] -= half
        self.pos[0][1] -= half
        self.pos[1][0] -= half
        self.pos[1][1] -= half

        self.width = self.pos[1][0] - self.pos[0][0] + 1
        self.height = self.pos[1][1] - self.pos[0][1] + 1

        self.align()

    def get_absolut_xy(self, rel_xy):
        x, y = rel_xy[0], rel_xy[1]
        x = round(x * (self.width / self.transform_to[0]) + self.pos[0][0])
        y = round(y * (self.height / self.transform_to[1]) + self.pos[0][1])
        return x, y

