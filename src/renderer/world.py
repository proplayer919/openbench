import pygame

from src.world.tile import Tile
from src.world.chunk import Chunk
from src.camera import Camera
from src.asset.pack_manager import PackManager
from src.asset.tile import TileTexture


class WorldRenderer:
    def __init__(self, pack_manager: PackManager, surface: pygame.Surface):
        self.pack_manager = pack_manager
        self.surface = surface
        # Cache for scaled pygame Surfaces keyed by (texture_id, quantized_zoom)
        # This avoids recreating Surfaces and repeatedly calling pygame.transform.scale
        # for every tile every frame.
        self._scaled_surface_cache: dict[tuple[str, float], pygame.Surface] = {}

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
        # Use already-converted pygame Surface from the pack manager and a
        # cached scaled version for the current zoom level so we don't
        # repeatedly convert PIL Images or rescale the same texture every tile.
        base_surface = self.pack_manager.load_texture_as_surface(tile.type)
        if base_surface is None:
            return  # Missing texture

        # Helper to quantize zoom so cache keys remain stable across tiny float
        # differences. 3 decimal places is enough for typical zoom values.
        def _zoom_key(z: float) -> float:
            return round(z, 3)

        zoom = camera.zoom
        zk = _zoom_key(zoom)
        cache_key = (tile.type, zk)

        if cache_key in self._scaled_surface_cache:
            scaled_surface = self._scaled_surface_cache[cache_key]
        else:
            w, h = base_surface.get_width(), base_surface.get_height()
            sw = max(1, int(w * zoom))
            sh = max(1, int(h * zoom))
            scaled_surface = pygame.transform.scale(base_surface, (sw, sh))
            self._scaled_surface_cache[cache_key] = scaled_surface

        # World to screen transformation (snap camera to avoid subpixel rendering)
        def round_1_16(val):
            return round(val * 16) / 16

        cam_px = round_1_16(camera.position[0])
        cam_py = round_1_16(camera.position[1])

        tile_x_rounded = round_1_16(tile_x)
        tile_y_rounded = round_1_16(tile_y)
        screen_x = int(((tile_x_rounded * base_surface.get_width()) - cam_px) * zoom)
        screen_y = int(((tile_y_rounded * base_surface.get_height()) - cam_py) * zoom)

        rect = pygame.Rect(
            screen_x, screen_y, scaled_surface.get_width(), scaled_surface.get_height()
        )
        self.surface.blit(scaled_surface, rect)

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

        # Get mouse position in screen coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate hovered tile position in world coordinates
        # Assume all tiles are 16x16 pixels (from TileTexture)
        zoom = camera.zoom
        cam_px = camera.position[0]
        cam_py = camera.position[1]
        tile_size = 16 * zoom
        hovered_tile_x = int((mouse_x / zoom + cam_px) // 16)
        hovered_tile_y = int((mouse_y / zoom + cam_py) // 16)

        hovered_screen_x = int(((hovered_tile_x * 16) - cam_px) * zoom)
        hovered_screen_y = int(((hovered_tile_y * 16) - cam_py) * zoom)
        hovered_rect = pygame.Rect(
            hovered_screen_x, hovered_screen_y, int(16 * zoom), int(16 * zoom)
        )

        # Iterate chunks and tiles, but use pre-converted pygame Surfaces and
        # cached scaled surfaces to avoid repeated conversion/scale operations.
        def _zoom_key(z: float) -> float:
            return round(z, 3)

        zk = _zoom_key(camera.zoom)
        for chunk in chunks:
            for tile in chunk.tiles:
                tile_x = tile.x + (16 * chunk.position[0])
                tile_y = tile.y + (16 * chunk.position[1])

                base_surface = self.pack_manager.load_texture_as_surface(tile.type)
                if base_surface is None:
                    continue

                cache_key = (tile.type, zk)
                if cache_key in self._scaled_surface_cache:
                    scaled_surface = self._scaled_surface_cache[cache_key]
                else:
                    w, h = base_surface.get_width(), base_surface.get_height()
                    sw = max(1, int(w * camera.zoom))
                    sh = max(1, int(h * camera.zoom))
                    scaled_surface = pygame.transform.scale(base_surface, (sw, sh))
                    self._scaled_surface_cache[cache_key] = scaled_surface

                screen_x = int(
                    ((tile_x * base_surface.get_width()) - camera.position[0])
                    * camera.zoom
                )
                screen_y = int(
                    ((tile_y * base_surface.get_height()) - camera.position[1])
                    * camera.zoom
                )
                rect = pygame.Rect(
                    screen_x,
                    screen_y,
                    scaled_surface.get_width(),
                    scaled_surface.get_height(),
                )
                self.surface.blit(scaled_surface, rect)

        # Draw selector texture on top of hovered tile (even if empty)
        selector_img = self.pack_manager.load_texture("openbench.selector")
        if selector_img is not None:
            selector_texture = TileTexture("openbench.selector", selector_img)
            selector_surface = pygame.transform.scale(
                selector_texture.surface, (hovered_rect.width, hovered_rect.height)
            )
            self.surface.blit(selector_surface, hovered_rect)
