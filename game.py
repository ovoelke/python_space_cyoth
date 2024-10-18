import pygame as pg

from player import Player

WINDOW_TITLE = 'Cyoth'
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_BG_COLOR = (0, 0, 0)
TILE_SIZE = 10
TILES_HORIZONTALLY = WINDOW_WIDTH // TILE_SIZE
TILES_VERTICALLY = WINDOW_HEIGHT // TILE_SIZE


class Game:
    def __init__(self, true=True):
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)
        self.surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.running = true
        self.player = Player(self.surface, 20, 30)
        self.mouse_move = None
        self.mouse_click = None

    def run(self):
        while self.running:
            self.main_loop()
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
                self.mouse_click = pg.mouse.get_pos()
            elif event.type == pg.MOUSEMOTION:
                self.mouse_move = pg.mouse.get_pos()

        if self.mouse_move:
            new_angle = self.player.get_angle(self.mouse_move)
            self.player.angle = new_angle

        if self.mouse_click:
            finish = self.player.move(self.mouse_click)
            if finish:
                self.mouse_click = None

        self.player.draw()

        pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
