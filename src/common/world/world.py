from src.common.world.tile import Tile
from src.common.world.chunk import Chunk
from src.common.logging import get_logger

logger = get_logger("openbench_common")


class World:
    def __init__(self, chunks: dict[str, Chunk] | None = None, spawn_location: tuple[int, int] = (0, 0)):
        self.chunks: dict[str, Chunk] = chunks if chunks is not None else {}
        self.spawn_location = spawn_location

    def add_chunk(self, chunk_id: str, chunk: Chunk):
        if chunk_id not in self.chunks:
            self.chunks[chunk_id] = chunk

    def get_chunk(self, chunk_id: str) -> Chunk | None:
        return self.chunks.get(chunk_id)

    def remove_chunk(self, chunk_id: str):
        if chunk_id in self.chunks:
            del self.chunks[chunk_id]
