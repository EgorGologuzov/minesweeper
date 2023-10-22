import pygame as pg
import area
import clickmanager
import panel_mod

pg.init()


root_width = 720         # Ширина окна
root_height = 620        # Высота окна
root = pg.display.set_mode((root_width, root_height))
pg.display.set_caption("SAPPER")
pg.display.set_icon(pg.image.load("sapper_sprites/mina (2).png"))
clock = pg.time.Clock()


def new_game():
    global main_area, panel, event_manager, addresses
    main_area = area.Area(root, addresses)
    panel = panel_mod.Panel(root, main_area.num_mines, (620, 0, 100, 620), addresses)
    event_manager = clickmanager.EventManager(main_area, panel)


addresses = {"new_game": new_game}

main_area = area.Area(root, addresses)
panel = panel_mod.Panel(root, main_area.num_mines, (620, 0, 100, 620), addresses)
event_manager = clickmanager.EventManager(main_area, panel)


while True:
    clock.tick(30)
    main_area.draw()
    panel.draw()
    pg.display.update()
    if event_manager.main(pg.event.get()):
        break
pg.quit()