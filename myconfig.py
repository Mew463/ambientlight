from dataclasses import dataclass
from enum import Enum

@dataclass
class MyDisplay:
    resolution: tuple
    colorOffset: list

    pixelSideOffset: int

    def getX(self):
        return self.resolution[0]
    def getY(self):
        return self.resolution[1]

    def printResolution(self):
        print(self.resolution[1])

@dataclass
class MyLeds:
    horizontal: int
    vertical: int  

    gpio_pin: int

    startSide: int
    isCounterClockwise: bool

    numLeds = 0

    def __post_init__(self):
        # Compute numLeds dynamically after initialization
        self.numLeds = 2 * self.horizontal + 2 * self.vertical

class Sides(Enum):
    RIGHT = 0
    TOP = 1
    LEFT = 2
    BOTTOM = 3



