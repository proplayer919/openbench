from src.atrribute import Attribute
from src.world.tile import Tile
from src.logging import get_logger

logger = get_logger()


class Physics:
    def __init__(self, entity, world_tiles: list[Tile]):
        self.entity = entity
        self.world_tiles = world_tiles

    def get_attr(self, key, default):
        return (
            self.entity.attributes[key].value
            if key in self.entity.attributes
            else default
        )

    def apply(self, dt: float = 1.0):
        # Gravity
        gravity = self.get_attr("gravity", 0.5)
        self.entity.velocity[1] += gravity * dt

        hitbox = self.entity.hitbox
        if not hitbox:
            # No hitbox, just update position
            self.entity.position = (
                self.entity.position[0] + self.entity.velocity[0] * dt,
                self.entity.position[1] + self.entity.velocity[1] * dt,
            )
            return

        # Predict new position
        orig_x, orig_y = self.entity.position
        vx, vy = self.entity.velocity
        new_x = orig_x + vx * dt
        new_y = orig_y + vy * dt

        # Helper: get AABB for entity at (x, y)
        def get_aabb(x, y):
            return (
                x,
                y,
                x + hitbox.width,
                y + hitbox.height,
            )

        # Helper: get AABB for tile
        def get_tile_aabb(tile: Tile):
            tx, ty = tile.x, tile.y
            return (tx, ty, tx + 1, ty + 1)

        # Check collisions for each axis separately (swept AABB)
        collided_x = False
        collided_y = False

        # Move X
        entity_aabb_x = get_aabb(new_x, new_y)
        for tile in self.world_tiles:
            tx, ty = getattr(tile, "x", None), getattr(tile, "y", None)
            if tx is None or ty is None:
                continue
            tile_aabb = get_tile_aabb(tile)
            if (
                entity_aabb_x[0] < tile_aabb[2]
                and entity_aabb_x[2] > tile_aabb[0]
                and entity_aabb_x[1] < tile_aabb[3]
                and entity_aabb_x[3] > tile_aabb[1]
            ):
                collided_x = True
                if vx > 0:
                    temp_x = tile_aabb[0] - hitbox.width
                elif vx < 0:
                    temp_x = tile_aabb[2]
                vx = 0
                break

        # Move Y
        entity_aabb_y = get_aabb(new_x, new_y)
        for tile in self.world_tiles:
            tx, ty = tile.x, tile.y
            if tx is None or ty is None:
                continue
            tile_aabb = get_tile_aabb(tile)
            if (
                entity_aabb_y[0] < tile_aabb[2]
                and entity_aabb_y[2] > tile_aabb[0]
                and entity_aabb_y[1] < tile_aabb[3]
                and entity_aabb_y[3] > tile_aabb[1]
            ):
                collided_y = True
                if vy > 0:
                    temp_y = tile_aabb[1] - hitbox.height
                elif vy < 0:
                    temp_y = tile_aabb[3]
                vy = 0
                break

        self.entity.position = (new_x, new_y)
        self.entity.velocity = [vx, vy]

        # On ground if collided downward with a solid tile
        self.entity.on_ground = collided_y and vy == 0 and orig_y < new_y

        logger.debug(
            f"Entity {self.entity.uuid} position: {self.entity.position}, velocity: {self.entity.velocity}, on_ground: {self.entity.on_ground}"
        )

    def move_left(self):
        self.entity.velocity[0] = -self.get_attr("move_speed", 5.0)

    def move_right(self):
        self.entity.velocity[0] = self.get_attr("move_speed", 5.0)

    def stop_horizontal(self):
        self.entity.velocity[0] = 0

    def jump(self):
        if self.entity.on_ground:
            self.entity.velocity[1] = -self.get_attr("jump_height", 10.0)
            self.entity.on_ground = False
