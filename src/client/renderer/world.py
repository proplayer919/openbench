import pygame

from src.common.world.tile import Tile
from src.common.world.chunk import Chunk
from src.common.camera import Camera
from src.client.asset.pack_manager import PackManager
from src.client.asset.tile import TileTexture


class WorldRenderer:
    def __init__(self, pack_manager: PackManager, surface: pygame.Surface):
        self.pack_manager = pack_manager
        self.surface = surface
        self._last_visible_tiles = set()

    def get_visible_tiles(self, chunks: list[Chunk], camera: Camera):
        cam_x, cam_y = camera.position
        zoom = camera.zoom
        view_w = self.surface.get_width() / zoom
        view_h = self.surface.get_height() / zoom
        visible = set()
        for chunk in chunks:
            for tile in chunk.tiles:
                tile_world_x = tile.x + (16 * chunk.position[0])
                tile_world_y = tile.y + (16 * chunk.position[1])
                if (cam_x <= tile_world_x < cam_x + view_w) and (
                    cam_y <= tile_world_y < cam_y + view_h
                ):
                    visible.add((tile_world_x, tile_world_y, tile.type))
        return visible

    def render_tile(self, tile: Tile, chunk_position: tuple[int, int], camera: Camera):
        tile_x = tile.x + (16 * chunk_position[0])
        tile_y = tile.y + (16 * chunk_position[1])

        texture_img = self.pack_manager.load_texture(tile.type)
        if texture_img is None:
            return  # Missing texture
        tile_texture = TileTexture(tile.type, texture_img)
        # Camera zoom: >1 means zoom in, <1 means zoom out
        # World to screen transformation
        # The tile position is scaled by zoom, so zoom=2.0 means 2x closer (bigger), zoom=0.5 means 2x farther (smaller)
        screen_x = int(
            ((tile_x * tile_texture.width) - camera.position[0]) * camera.zoom
        )
        screen_y = int(
            ((tile_y * tile_texture.height) - camera.position[1]) * camera.zoom
        )
        # The tile size is also scaled by zoom
        tile_w = int(tile_texture.width * camera.zoom)
        tile_h = int(tile_texture.height * camera.zoom)
        rect = pygame.Rect(screen_x, screen_y, tile_w, tile_h)
        self.surface.blit(
            pygame.transform.scale(tile_texture.surface, (tile_w, tile_h)), rect
        )

    def render_chunk(self, chunk: Chunk, camera: Camera):
        # Culling: only render tiles in camera view
        cam_x, cam_y = camera.position
        view_w = self.surface.get_width() / camera.zoom
        view_h = self.surface.get_height() / camera.zoom
        for tile in chunk.tiles:
            tile_world_x = tile.x + (16 * chunk.position[0])
            tile_world_y = tile.y + (16 * chunk.position[1])
            if (cam_x <= tile_world_x < cam_x + view_w) and (
                cam_y <= tile_world_y < cam_y + view_h
            ):
                self.render_tile(tile, chunk.position, camera)

    def render_chunks(self, chunks: list[Chunk], camera: Camera):
        # Always fill background to avoid flicker
        self.surface.fill((0, 0, 0))
        visible_now = self.get_visible_tiles(chunks, camera)
        changed_tiles = visible_now.symmetric_difference(self._last_visible_tiles)
        rects_to_update = []
        for chunk in chunks:
            for tile in chunk.tiles:
                tile_world_x = tile.x + (16 * chunk.position[0])
                tile_world_y = tile.y + (16 * chunk.position[1])
                key = (tile_world_x, tile_world_y, tile.type)
                if key in changed_tiles or not self._last_visible_tiles:
                    # Redraw changed or first frame
                    tile_x = tile.x + (16 * chunk.position[0])
                    tile_y = tile.y + (16 * chunk.position[1])
                    texture_img = self.pack_manager.load_texture(tile.type)
                    if texture_img is None:
                        continue
                    tile_texture = TileTexture(tile.type, texture_img)
                    screen_x = int(
                        ((tile_x * tile_texture.width) - camera.position[0])
                        * camera.zoom
                    )
                    screen_y = int(
                        ((tile_y * tile_texture.height) - camera.position[1])
                        * camera.zoom
                    )
                    tile_w = int(tile_texture.width * camera.zoom)
                    tile_h = int(tile_texture.height * camera.zoom)
                    rect = pygame.Rect(screen_x, screen_y, tile_w, tile_h)
                    self.surface.blit(
                        pygame.transform.scale(tile_texture.surface, (tile_w, tile_h)),
                        rect,
                    )
                    rects_to_update.append(rect)
        self._last_visible_tiles = visible_now
        if rects_to_update:
            pygame.display.update(rects_to_update)
