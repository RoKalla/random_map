from enum import Enum, auto
from dataclasses import dataclass


class TileType(Enum):
    LAND = auto()
    WATER = auto()
    FOREST = auto()

class TileColor(Enum):
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    DARK_GREEN = [34, 139, 34]

type_color_map = {
    TileType.LAND: TileColor.GREEN,
    TileType.WATER: TileColor.BLUE,
    TileType.FOREST: TileColor.DARK_GREEN
}

@dataclass
class Tile:
    type: TileType
    x: int
    y: int
    _color: TileColor = None

    def __post_init__(self):
        self._color = type_color_map[self.type]

    @property
    def color(self):
        return self._color.value
    
    def set_type(self, type: TileType):
        self.type = type
        self._color = type_color_map[type]