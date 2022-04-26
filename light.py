import numpy as np


class Light:
    def __init__(self, position) -> None:
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]