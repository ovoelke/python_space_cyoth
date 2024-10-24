from models.base_node import BaseNode


class ShootNode(BaseNode):
    def __init__(self, location, target=None, speed=5,angle=0, die_on_target=True):
        super().__init__(location, target, speed, angle, die_on_target)