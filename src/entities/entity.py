from src.errors import InvalidEntityDataError
from src.logging import get_logger
from src.atrribute import Attribute
from src.entities.hitbox import Hitbox
from src.entities.physics import Physics

logger = get_logger("openbench_common")


class Entity:
    def __init__(
        self,
        uuid: str,
        texture_id: str = "openbench.missing",
        hitbox: Hitbox | None = None,
        position: tuple[float, float] = (0, 0),
        attributes: dict[str, Attribute] | None = None,
    ):
        if not uuid or not isinstance(uuid, str):
            logger.error(
                "InvalidEntityDataError: Entity UUID must be a non-empty string."
            )
            raise InvalidEntityDataError("Entity UUID must be a non-empty string.")

        self.uuid: str = uuid

        if not texture_id or not isinstance(texture_id, str):
            logger.error(
                "InvalidEntityDataError: Texture ID must be a non-empty string."
            )
            raise InvalidEntityDataError("Texture ID must be a non-empty string.")

        self.texture_id: str = texture_id

        if hitbox is not None and not isinstance(hitbox, Hitbox):
            logger.error(
                "InvalidEntityDataError: Hitbox must be an instance of Hitbox class."
            )
            raise InvalidEntityDataError("Hitbox must be an instance of Hitbox class.")

        self.hitbox: Hitbox | None = hitbox

        if not isinstance(position, (tuple, list)) or len(position) != 2:
            logger.error(
                "InvalidEntityDataError: Position must be a tuple of two integers."
            )
            raise InvalidEntityDataError("Position must be a tuple of two integers.")

        self.position: tuple[float, float] = position

        for attr_id, attr in (attributes or {}).items():
            if not isinstance(attr, Attribute):
                logger.error(
                    f"InvalidEntityDataError: Attribute {attr_id} must be an instance of Attribute class."
                )
                raise InvalidEntityDataError(
                    f"Attribute {attr_id} must be an instance of Attribute class."
                )

        self.attributes: dict[str, Attribute] = attributes or {}

        # Physics properties
        self.velocity = [0.0, 0.0]  # [vx, vy]
        self.on_ground = False
        self.physics: Physics | None = (
            None  # To be set externally with Physics(self, world_tiles)
        )
