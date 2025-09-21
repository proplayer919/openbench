from src.errors import InvalidPlayerDataError
from src.logging import get_logger
from src.entities.entity import Entity
from src.entities.hitbox import Hitbox
from src.atrribute import Attribute

logger = get_logger("openbench_common")


class Player(Entity):
    def __init__(
        self,
        uuid: str,
        username: str,
        position: tuple[int, int] = (0, 0),
        attributes: dict[str, Attribute] | None = None,
    ):
        if not uuid or not isinstance(uuid, str):
            logger.error(
                "InvalidPlayerDataError: Player UUID must be a non-empty string."
            )
            raise InvalidPlayerDataError("Player UUID must be a non-empty string.")

        if not username or not isinstance(username, str):
            logger.error("InvalidPlayerDataError: Username must be a non-empty string.")
            raise InvalidPlayerDataError("Username must be a non-empty string.")

        super().__init__(
            uuid, "openbench.player", Hitbox(1.0, 2.0), position, attributes
        )

        self.username: str = username
