from src.logging import get_logger
from src.errors import InvalidHitboxDataError

logger = get_logger("openbench_common")


class Hitbox:
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            logger.error(
                "InvalidHitboxDataError: Hitbox dimensions must be positive numbers."
            )
            raise InvalidHitboxDataError("Hitbox dimensions must be positive numbers.")
        self.width = width
        self.height = height
        self.area = width * height
        self.perimeter = 2 * (width + height)
        self.center = (width / 2, height / 2)

    def contains_point(self, x: float, y: float) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height

    def resize(self, new_width: float, new_height: float):
        if new_width <= 0 or new_height <= 0:
            raise InvalidHitboxDataError(
                "InvalidHitboxDataError: Hitbox dimensions must be positive numbers."
            )
        self.width = new_width
        self.height = new_height
        self.area = new_width * new_height
        self.perimeter = 2 * (new_width + new_height)
        self.center = (new_width / 2, new_height / 2)
