import pygame as pg
from pygame import Vector2, Color

from models.player_node import PlayerNode
from models.shoot_node import ShootNode
from network_manager import NetworkManager
from settings import *

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(WINDOW_TITLE)
        self.running = True
        self.clock = pg.time.Clock()
        self.surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.player = PlayerNode(Vector2(20, 20))
        self.player_opponents = {}
        self.shoots = []
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
                if event.button == 3: #right mouse button
                    self.player.target = Vector2(event.pos[0], event.pos[1])
                    if self.network_manager.is_running:
                        self.network_manager.send_data(self.player)
                if event.button == 1: #left mouse button
                    self.shoots.append(ShootNode(self.player.location, Vector2(event.pos[0], event.pos[1]), die_on_target=True))
            elif event.type == pg.MOUSEMOTION:
                self.mouse_pos_move = pg.mouse.get_pos()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    # Key s: start server
                    pg.display.set_caption(
                        f"{WINDOW_TITLE} - Server - {self.network_manager.host}:{self.network_manager.port}")
                    self.network_manager.start_server()
                elif event.key == pg.K_c:
                    # Key c: connect to server
                    pg.display.set_caption(
                        f"{WINDOW_TITLE} - Client - {self.network_manager.host}:{self.network_manager.port}")
                    self.network_manager.connect_to_server()

        self.player.update_position()
        self.draw_player(self.player, COLOR_BLUE)

        # todo: i don't know if this is necessary...
        # update opponents from network manager with local opponents
        for key in self.network_manager.opponents:
            unit = self.network_manager.opponents[key]
            if unit not in self.player_opponents:
                # add
                self.player_opponents = {key: unit}
            else:
                # refresh
                self.player_opponents[key].location = unit.location
                self.player_opponents[key].target = unit.target

        # update shoots
        for shoot in self.shoots:
            shoot.update_position()
            if shoot.alive is not True:
                self.shoots.remove(shoot)
            else:
                self.draw_shoot(shoot, COLOR_GREEN)
        
        # draw every opponent
        for opponent in self.player_opponents.values():
            opponent.update_position()
            self.draw_player(opponent, COLOR_RED)
            
        pg.display.set_caption(f"{WINDOW_TITLE} - Shoots: {len(self.shoots)}")

        pg.display.update()
        self.clock.tick(60)

    def draw_player(self, node: PlayerNode, color: Color):
        # line between unit and target
        pg.draw.line(self.surface, COLOR_GREEN, node.location, node.target, 1)

        # draw unit
        pg.draw.circle(self.surface, color, node.location, 10)
    
    
    def draw_shoot(self, node: ShootNode, color: Color):
        # line between unit and target
        pg.draw.line(self.surface, COLOR_BLUE, node.location, node.target, 1)

        # draw unit
        pg.draw.circle(self.surface, color, node.location, 5)


if __name__ == '__main__':
    game = Game()
    game.run()
