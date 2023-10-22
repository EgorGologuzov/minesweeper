import pygame as pg
import settings


class Button:
    def __init__(self, rect, sprite_address, surf):
        self.rect = pg.rect.Rect(rect)
        self.surf = surf
        self.sprite = pg.transform.scale(pg.image.load(sprite_address), self.rect.size)
        self.past_aiming = False

    def check_aiming(self, xy):
        def inside(rect, point):
            x1 = rect.x
            y1 = rect.y
            x2 = rect.width + x1
            y2 = rect.height + y1
            return (point[0] >= x1) and (point[0] < x2) and (point[1] >= y1) and (point[1] < y2)

        if inside(self.rect, xy):
            if not self.past_aiming:
                self.rect.x += 2
                self.rect.y += 2
            self.past_aiming = True
            return True
        elif self.past_aiming:
            self.rect.x -= 2
            self.rect.y -= 2
            self.past_aiming = False
        return False

    def draw(self):
        self.surf.blit(self.sprite, self.rect)


class Panel:
    def __init__(self, main_display_link, num_flags, rect, addresses):
        self.rect = pg.rect.Rect(rect[0], rect[1], rect[2], rect[3])
        self.surf = pg.Surface((self.rect.w, self.rect.h))
        self.num_flags = num_flags
        self.main_display_link = main_display_link
        self.font = pg.font.SysFont("Arial", 25)
        self.font_c = pg.color.Color(50, 50, 50, 255)
        self.bg_c = pg.color.Color(170, 170, 170, 255)
        self.game_stat = 2  # 1 - игрок проиграл, 2 - игра идет, 3 - игра окончена (все клетки кроме мин открыты)
        self.sprites = [pg.image.load("sapper_sprites/flag_wb.png"), pg.image.load("sapper_sprites/defeat.png"),
                        pg.image.load("sapper_sprites/run.png"), pg.image.load("sapper_sprites/finish.png")]
        self.time = 0
        self.timer_on = True
        self.past_tick = pg.time.get_ticks()
        self.address = addresses
        self.address["panel"] = self
        self.btn_repl = Button((10, 100, 80, 30), "sapper_sprites/btn_replay.png", self.surf)
        self.btn_settings = Button((10, 200, 80, 30), "sapper_sprites/btn_settings.png", self.surf)
        self.settings_menu = None

    def draw(self):
        self.surf.fill(self.bg_c)
        self.surf.blit(self.sprites[0], (5, 5))
        render = self.font.render(f"{self.num_flags}", True, self.font_c, self.bg_c)

        if (pg.time.get_ticks() - self.past_tick) > 1000 and self.timer_on and self.time < 1000:
            self.past_tick = pg.time.get_ticks()
            self.time += 1
        time_ren = self.font.render(f"{self.time}", True, self.font_c, self.bg_c)
        self.surf.blit(render, render.get_rect(center=(68, 25)))
        self.surf.blit(time_ren, time_ren.get_rect(center=(50, 65)))
        self.btn_repl.draw()
        self.btn_settings.draw()
        self.surf.blit(self.sprites[self.game_stat], self.sprites[self.game_stat].get_rect(center=(50, 160)))
        self.main_display_link.blit(self.surf, self.rect)

    def get_rect(self):
        return self.rect

    def stop_game(self, stat):
        if stat == "win":
            self.game_stat = 3
            self.timer_on = False
        elif stat == "def":
            self.game_stat = 1
            self.timer_on = False

    def set_motion(self, xy, vec):
        self.btn_repl.check_aiming((xy[0] - self.rect.x, xy[1] - self.rect.y))
        self.btn_settings.check_aiming((xy[0] - self.rect.x, xy[1] - self.rect.y))

    def set_click(self, xy, btn):
        if btn == 1:
            if self.btn_repl.check_aiming((xy[0] - self.rect.x, xy[1] - self.rect.y)):
                self.address["new_game"]()
            elif self.btn_settings.check_aiming((xy[0] - self.rect.x, xy[1] - self.rect.y)):
                self.settings_menu = settings.SettingsMenu()

    def set_down(self, xy, btn):
        None



