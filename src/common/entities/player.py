from src.common.errors import InvalidPlayerDataError
from src.common.logging import get_logger
from src.common.entities.entity import Entity
from src.common.entities.hitbox import Hitbox
from src.common.atrribute import Attribute

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
        self.player_mode: str = "default"  # Mode: "default", "editor", or "viewer"
        self.allow_flight: bool = False
        self.is_flying: bool = False
