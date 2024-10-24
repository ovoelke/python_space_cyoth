from models.base_node import BaseNode


class PlayerNode(BaseNode):
    def __init__(self, location, target=None, speed=0.5,angle=0, die_on_target=False):
        super().__init__(location, target, speed, angle, die_on_target)