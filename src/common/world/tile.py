from typing import Optional


class Tile:
    def __init__(self, x: int, y: int, type: str, block_state: Optional[dict] = None):
        self.x = x
        self.y = y
        self.type = type
        self.block_state = block_state if block_state is not None else {}
