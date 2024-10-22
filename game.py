import pygame as pg
from pygame import Vector2, Color

from models.unit import Unit
from network_manager import NetworkManager
from settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(WINDOW_TITLE)
        self.running = True
        self.clock = pg.time.Clock()
        self.surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.player = Unit(Vector2(20, 20))
        self.player_opponents = {}
        self.mouse_pos_move = None
        self.mouse_pos_click = None
        self.network_manager = NetworkManager()

    def run(self):
        while self.running:
            self.main_loop()

        if self.network_manager.is_running:
            self.network_manager.stop()

        pg.quit()

    def main_loop(self):
        self.surface.fill(WINDOW_BG_COLOR)
        for row in range(TILES_VERTICALLY):
            for col in range(TILES_HORIZONTALLY):
                alt = (row + col) % 2 == 0
                color = (32, 32, 32) if alt else (48, 48, 48)
                pg.draw.rect(
                    self.surface,
                    color,
                    (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                )
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONUP:
                self.player.target = Vector2(event.pos[0], event.pos[1])
                if self.network_manager.is_running:
                    self.network_manager.send_data(self.player)
            elif event.type == pg.MOUSEMOTION:
                self.mouse_pos_move = pg.mouse.get_pos()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    # Key s: start server
                    self.network_manager.start_server()
                elif event.key == pg.K_c:
                    # Key c: connect to server
                    self.network_manager.connect_to_server()

        self.player.update_position()
        self.draw_unit(self.player, 'green')

        # todo: i don't know if this is necessary...
        # update opponents from network manager with local opponents
        for key in self.network_manager.opponents:
            unit =  self.network_manager.opponents[key]
            if unit not in self.player_opponents:
                #add
                self.player_opponents = {key: unit}
            else:
                #refresh
                self.player_opponents[key].location = unit.location
                self.player_opponents[key].target = unit.target

        # draw every opponent
        for opponent in self.player_opponents.values():
            opponent.update_position()
            self.draw_unit(opponent, 'blue')

        pg.display.update()
        self.clock.tick(60)

    def draw_unit(self, unit: Unit, color: Color):
        # line between unit and target
        pg.draw.line(self.surface, pg.Color('yellow'), unit.location, unit.target, 1)

        # draw unit
        pg.draw.circle(self.surface, pg.Color('red'), unit.location, 10)


if __name__ == '__main__':
    game = Game()
    game.run()
