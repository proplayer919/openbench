import pygame

from src.entities.entity import Entity
from src.entities.hitbox import Hitbox
from src.camera import Camera
from src.asset.pack_manager import PackManager
from src.errors import MissingTextureError
from src.logging import get_logger

logger = get_logger()


class EntityRenderer:
    def __init__(self, pack_manager: PackManager, surface: pygame.Surface):
        self.pack_manager = pack_manager
        self.surface = surface

    def render_entity(self, entity: Entity, camera: Camera):
        logger.debug(
            f"Rendering entity {entity.uuid} at world position {entity.position}"
        )

        # Determine texture
        texture_id = entity.texture_id
        logger.debug(f"Entity {entity.uuid} uses texture ID: {texture_id}")
        texture_img = self.pack_manager.load_texture_as_surface(texture_id)
        if texture_img is None:
            logger.error(
                f"MissingTextureError: Missing texture for entity {entity.uuid}: {texture_id}"
            )
            raise MissingTextureError(f"Missing texture for ID: {texture_id}")

        # Assume entity has hitbox for size
        hitbox = entity.hitbox
        if hitbox:
            logger.debug(
                f"Entity {entity.uuid} hitbox size: {hitbox.width}x{hitbox.height} (in tiles) / {hitbox.width * 16}x{hitbox.height * 16} (in pixels)"
            )
            width = hitbox.width * 16
            height = hitbox.height * 16
        else:
            logger.debug(
                f"Entity {entity.uuid} has no hitbox, using default size: 1x1 tile / 16x16 pixels"
            )
            width = 16
            height = 16

        # World to screen transformation
        def round_1_16(val):
            return round(val * 16) / 16

        cam_x = round_1_16(camera.position[0])
        cam_y = round_1_16(camera.position[1])
        ent_x = round_1_16(entity.position[0])
        ent_y = round_1_16(entity.position[1])
        screen_x = int((ent_x - cam_x) * camera.zoom)
        screen_y = int((ent_y - cam_y) * camera.zoom)
        entity_w = int(width * camera.zoom)
        entity_h = int(height * camera.zoom)
        logger.debug(
            f"Entity {entity.uuid} screen position: ({screen_x}, {screen_y}), size: ({entity_w}x{entity_h}), camera zoom: {camera.zoom}"
        )
        rect = pygame.Rect(screen_x, screen_y, entity_w, entity_h)

        logger.debug(f"Blitting entity {entity.uuid} to surface at rect {rect}")
        self.surface.blit(
            pygame.transform.scale(texture_img, (entity_w, entity_h)), rect
        )

    def render_entities(self, entities: list[Entity], camera: Camera):
        cam_x, cam_y = camera.position
        cam_w = self.surface.get_width()
        cam_h = self.surface.get_height()
        zoom = camera.zoom
        # Camera view rectangle in world coordinates
        view_rect = pygame.Rect(cam_x, cam_y, cam_w / zoom, cam_h / zoom)
        for entity in entities:
            # Get entity position and size
            pos = getattr(entity, "position", (0, 0))
            hitbox = getattr(entity, "hitbox", None)
            if hitbox:
                width = hitbox.width * 16
                height = hitbox.height * 16
            else:
                width = 16
                height = 16
            entity_rect = pygame.Rect(pos[0], pos[1], width, height)
            if view_rect.colliderect(entity_rect):
                self.render_entity(entity, camera)
