from src.common.errors import InvalidNonPlayerEntityDataError, InvalidPlayerDataError
from src.common.logging import get_logger
from src.common.entities.entity import Entity
from src.common.entities.hitbox import Hitbox
from src.common.atrribute import Attribute

logger = get_logger("openbench_common")


class NonPlayerEntity(Entity):
    def __init__(
        self,
        uuid: str,
        texture_id: str = "openbench.missing",
        hitbox: Hitbox | None = None,
        position: tuple[int, int] = (0, 0),
        attributes: dict[str, Attribute] | None = None,
    ):
        if not uuid or not isinstance(uuid, str):
            logger.error(
                "InvalidNonPlayerEntityDataError: Non-Player Entity UUID must be a non-empty string."
            )
            raise InvalidNonPlayerEntityDataError(
                "Non-Player Entity UUID must be a non-empty string."
            )

        if not uuid.startswith("#"):
            logger.error(
                "InvalidNonPlayerEntityDataError: Non-Player Entity UUID must start with '#'."
            )
            raise InvalidNonPlayerEntityDataError(
                "Non-Player Entity UUID must start with '#'."
            )

        super().__init__(uuid, texture_id, hitbox, position, attributes)
