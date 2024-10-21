import pygame as pg

from settings import *
from player import Player
from network_manager import NetworkManager


class Game:
    def __init__(self):
        self.running = True
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)
        self.surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player = Player(self.surface, 20, 30)
        self.mouse_pos_move = None
        self.mouse_pos_click = None
        self.mouse_pos_click_before = None
        self.network_manager = NetworkManager()

    def run(self):
        while self.running:
            self.main_loop()

        if self.network_manager.is_active:
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
                self.mouse_pos_click = pg.mouse.get_pos()
            elif event.type == pg.MOUSEMOTION:
                self.mouse_pos_move = pg.mouse.get_pos()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    # s => start server
                    self.network_manager.start_server()
                elif event.key == pg.K_c:
                    # c => connect to server
                    self.network_manager.connect_to_server()

        if self.mouse_pos_move:
            new_angle = self.player.get_angle(self.mouse_pos_move)
            self.player.angle = new_angle

        if self.mouse_pos_click:
            # updating position...
            if self.mouse_pos_click_before is not self.mouse_pos_click:
                self.mouse_pos_click_before = self.mouse_pos_click
                self.network_manager.send_data(self.mouse_pos_click)

            player_halted = self.player.move(self.mouse_pos_click)
            if player_halted:
                self.mouse_pos_click = None # ...clear position

        if self.network_manager.is_server and len(self.network_manager.clients) > 0:
            print(f'clients: {len(self.network_manager.clients)}')

        self.player.draw()
        pg.display.update()

        self.clock.tick(30)


if __name__ == '__main__':
    game = Game()
    game.run()
