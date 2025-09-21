from src.world.tile import Tile
from src.errors import InvalidChunkDataError
from src.logging import get_logger

logger = get_logger("openbench_common")


class Chunk:
    def __init__(self, position: tuple[int, int], tiles: list[Tile]):
        # Validate chunk data
        if not tiles:
            raise InvalidChunkDataError("Chunk must contain at least one tile.")

        self.position = position
        self.tiles = tiles
        self.chunk_id_string = f"{position[0]}.{position[1]}"
