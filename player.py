import math

import pygame as pg

PLAYER_STEP_WIDTH = 0.15
PLAYER_ANGLE_LINE_LENGTH = 15


class Player:
    def __init__(self, surface, start_x, start_y):
        self.surface = surface
        self.x = start_x
        self.y = start_y
        self.angle = 45.0

    def draw(self):
        pg.draw.circle(self.surface, pg.Color('red'), (self.x, self.y), 5)

        end_x = self.x + PLAYER_ANGLE_LINE_LENGTH * math.cos(self.angle)
        end_y = self.y + PLAYER_ANGLE_LINE_LENGTH * math.sin(self.angle)
        pg.draw.aaline(self.surface, pg.Color('red'), (self.x, self.y), (end_x, end_y))

    def move(self, target:[int,int]) -> bool:
        delta_x = target[0] - self.x
        delta_y = target[1] - self.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if distance > PLAYER_STEP_WIDTH:
            move_x = (delta_x / distance) * PLAYER_STEP_WIDTH
            move_y = (delta_y / distance) * PLAYER_STEP_WIDTH
            self.x += move_x
            self.y += move_y
            return False
        else:
            self.x = target[0]
            self.y = target[1]
            return True

    def get_angle(self, target):
        return math.atan2(target[1] - self.y, target[0] - self.x)
