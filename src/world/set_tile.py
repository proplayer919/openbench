from src.world.tile import Tile
from src.world.chunk import Chunk


def set_tile(chunks, world_x, world_y, tile_type):
    tile_x = int(world_x // 16)
    tile_y = int(world_y // 16)
    chunk_x = tile_x // 16
    chunk_y = tile_y // 16
    local_x = tile_x % 16
    local_y = tile_y % 16
    # Find chunk by position
    found_chunk = None
    for chunk in chunks:
        if chunk.position == (chunk_x, chunk_y):
            found_chunk = chunk
            break
    found_tile = None
    if found_chunk:
        for tile in found_chunk.tiles:
            if tile.x == local_x and tile.y == local_y:
                found_tile = tile
                break
        if tile_type is None:
            if found_tile:
                found_chunk.tiles.remove(found_tile)
                if not found_chunk.tiles:
                    chunks.remove(found_chunk)
            return found_chunk, None
        if not found_tile:
            found_tile = Tile(local_x, local_y, tile_type)
            found_chunk.tiles.append(found_tile)
        else:
            found_tile.type = tile_type
        return found_chunk, found_tile
    else:
        if tile_type is None:
            return None, None
        # Create chunk with the new tile
        found_tile = Tile(local_x, local_y, tile_type)
        found_chunk = Chunk((chunk_x, chunk_y), [found_tile])
        chunks.append(found_chunk)
        return found_chunk, found_tile
