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

        # World to screen transformation
        # Snap camera position to integer pixels to avoid subpixel rendering
        def round_1_16(val):
            return round(val * 16) / 16

        cam_px = round_1_16(camera.position[0])
        cam_py = round_1_16(camera.position[1])
        zoom = camera.zoom

        # Calculate screen position and size, force integer pixel alignment
        tile_x_rounded = round_1_16(tile_x)
        tile_y_rounded = round_1_16(tile_y)
        screen_x = int(((tile_x_rounded * tile_texture.width) - cam_px) * zoom)
        screen_y = int(((tile_y_rounded * tile_texture.height) - cam_py) * zoom)
        tile_w = int(tile_texture.width * zoom)
        tile_h = int(tile_texture.height * zoom)

        # Always use scale for pixel art
        scaled_surface = pygame.transform.scale(tile_texture.surface, (tile_w, tile_h))

        # Inset by 1 pixel to avoid edge bleeding (optional, can be tuned)
        rect = pygame.Rect(screen_x, screen_y, tile_w, tile_h)
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

        for chunk in chunks:
            for tile in chunk.tiles:
                tile_x = tile.x + (16 * chunk.position[0])
                tile_y = tile.y + (16 * chunk.position[1])
                texture_img = self.pack_manager.load_texture(tile.type)
                if texture_img is None:
                    continue
                tile_texture = TileTexture(tile.type, texture_img)
                screen_x = int(
                    ((tile_x * tile_texture.width) - camera.position[0]) * camera.zoom
                )
                screen_y = int(
                    ((tile_y * tile_texture.height) - camera.position[1]) * camera.zoom
                )
                tile_w = int(tile_texture.width * camera.zoom)
                tile_h = int(tile_texture.height * camera.zoom)
                rect = pygame.Rect(screen_x, screen_y, tile_w, tile_h)
                self.surface.blit(
                    pygame.transform.scale(tile_texture.surface, (tile_w, tile_h)),
                    rect,
                )

        # Draw selector texture on top of hovered tile (even if empty)
        selector_img = self.pack_manager.load_texture("openbench.selector")
        if selector_img is not None:
            selector_texture = TileTexture("openbench.selector", selector_img)
            selector_surface = pygame.transform.scale(
                selector_texture.surface, (hovered_rect.width, hovered_rect.height)
            )
            self.surface.blit(selector_surface, hovered_rect)
