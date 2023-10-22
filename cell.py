

class Cell:

    """pos - позиция клетки на поле, owner - владелец клетки (нужен для вычисления относительного положения),
    num - значение клетки (кол-во мин вокруг), lid - состояние крышки (# - закрыта, * - открыта,
    f - стоит флаг), pos_px - относительная позиция в окне"""

    def __init__(self, pos, owner):
        self.pos = pos
        self.owner = owner
        self.num = 0
        self.lid = "#"
        self.pos_px = (self.pos[1] * self.owner.cell_width,
                       self.pos[0] * self.owner.cell_width)

    def mine_around(self):
        if self.num != 9:
            self.num += 1

    def become_mine(self):
        def send_mes(x, y):
            if (x >= 0) and (x < self.owner.width) and (y >= 0) and (y < self.owner.height):
                self.owner.MAP[y][x].mine_around()

        self.num = 9
        y, x = self.pos[1], self.pos[0]
        send_mes(y - 1, x - 1)
        send_mes(y - 1, x)
        send_mes(y - 1, x + 1)
        send_mes(y, x - 1)
        send_mes(y, x + 1)
        send_mes(y + 1, x - 1)
        send_mes(y + 1, x)
        send_mes(y + 1, x + 1)

    def you_clicking(self, btn):
        if self.lid != "*":
            if btn == 1:
                if self.lid == "f":
                    self.lid = "#"
                    self.owner.address["panel"].num_flags += 1
                else:
                    if self.num == 9:
                        self.owner.stop_game("def")
                    self.open()
            elif btn == 3:
                if self.lid != "f":
                    self.lid = "f"
                    self.owner.address["panel"].num_flags -= 1
                else:
                    self.lid = "#"
                    self.owner.address["panel"].num_flags += 1
            self.draw()

    def open(self):
        if self.lid == "#" and self.lid != 9:
            self.lid = "*"
            if self.num == 0:
                y, x = self.pos[0], self.pos[1]
                if y > 0:
                    self.owner.MAP[y - 1][x].open()
                if (y > 0) and (x < self.owner.width - 1):
                    self.owner.MAP[y - 1][x + 1].open()
                if x < self.owner.width - 1:
                    self.owner.MAP[y][x + 1].open()
                if (x < self.owner.width - 1) and (y < self.owner.height - 1):
                    self.owner.MAP[y + 1][x + 1].open()
                if y < self.owner.height - 1:
                    self.owner.MAP[y + 1][x].open()
                if (y < self.owner.height - 1) and (x > 0):
                    self.owner.MAP[y + 1][x - 1].open()
                if x > 0:
                    self.owner.MAP[y][x - 1].open()
                if (x > 0) and (y > 0):
                    self.owner.MAP[y - 1][x - 1].open()
        self.draw()

    def draw(self):
        if self.lid == "*":
            self.owner.root.blit(self.owner.sprites[self.num], self.pos_px)
        else:
            if self.lid == "#":
                self.owner.root.blit(self.owner.sprites[10], self.pos_px)
            else:
                self.owner.root.blit(self.owner.sprites[11], self.pos_px)



