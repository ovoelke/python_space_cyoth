import math
import uuid
from pygame import Vector2


class BaseNode:
    def __init__(self, location: Vector2, target: Vector2 | None = None, speed=1.0, angle=0, die_on_target=False):
        self.name = str(uuid.uuid4())
        self.location = location
        self.target = location if target is None else target
        self.speed = speed
        self.angle = angle
        self.die_on_target = die_on_target
        self.alive = True

    def update_position(self):
        if self.target is not None:
            distance = BaseNode.get_distance(self.location, self.target)
            if distance > self.speed:
                delta = BaseNode.get_delta(self.location, self.target)
                move_x = (delta[0] / distance) * self.speed
                move_y = (delta[1] / distance) * self.speed
                self.location = Vector2(self.location[0] + move_x, self.location[1] + move_y)
            else:
                if self.die_on_target:
                    self.alive = False

    @staticmethod
    def get_distance(location: Vector2, target: Vector2) -> float:
        delta = BaseNode.get_delta(location, target)
        return math.sqrt(delta[0] * delta[0] + delta[1] * delta[1])

    @staticmethod
    def get_delta(location: Vector2, target: Vector2) -> Vector2:
        return Vector2((target[0] - location[0]), (target[1] - location[1]))