import pygame as pg


class EventManager():
    def __init__(self, area, panel):
        self.down_pos = None
        self.up_pos = None
        self.area = area
        self.panel = panel
        self.past_pos = None
        self.down_time = None

    def main(self, event_list):
        def inside(rect, point):
            x1 = rect.x
            y1 = rect.y
            x2 = rect.width
            y2 = rect.height
            return (point[0] >= x1) and (point[0] < x2) and (point[1] >= y1) and (point[1] < y2)
        if inside(self.area.get_rect(), pg.mouse.get_pos()):
            recipient = self.area
        else:                           # inside(self.panel.get_rect(), pg.mouse.get_pos()):
            recipient = self.panel

        for event in event_list:
            if event.type == pg.QUIT:
                return True
            elif event.type == pg.MOUSEBUTTONUP:
                if (pg.time.get_ticks() - self.down_time) < 300:
                    recipient.set_click(pg.mouse.get_pos(), event.button)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.down_time = pg.time.get_ticks()
                recipient.set_down(pg.mouse.get_pos(), event.button)
            elif event.type == pg.MOUSEMOTION:
                new_pos = pg.mouse.get_pos()
                if self.past_pos is None:
                    self.past_pos = new_pos
                recipient.set_motion(new_pos, (new_pos[0] - self.past_pos[0], new_pos[1] - self.past_pos[1]))
                self.past_pos = new_pos

        if self.area.check_on_finish() and self.panel.game_stat != 1:
            self.panel.game_stat = 3
            self.area.stop_game("win")




