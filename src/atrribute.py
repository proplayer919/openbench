from src.errors import InvalidAttributeError
from src.logging import get_logger

logger = get_logger("openbench_common")


class Attribute:
    def __init__(self, id: str, value: float):
        if not id or not isinstance(id, str):
            logger.error(
                "InvalidAttributeError: Attribute id must be a non-empty string."
            )
            raise InvalidAttributeError("Attribute id must be a non-empty string.")

        if not isinstance(value, (float)):
            logger.error("InvalidAttributeError: Attribute value must be a float.")
            raise InvalidAttributeError("Attribute value must be a float.")

        self.id: str = id
        self.value: float = value
        self.min_value: float = -(10.0**10.0)
        self.max_value: float = 10.0**10.0

    def set_value(self, new_value: float):
        if not isinstance(new_value, float):
            logger.error("InvalidAttributeError: New attribute value must be a float.")
            raise InvalidAttributeError("New attribute value must be a float.")

        if not (self.min_value <= new_value <= self.max_value):
            logger.error(
                f"InvalidAttributeError: New attribute value {new_value} must be between {self.min_value} and {self.max_value}."
            )
            raise InvalidAttributeError(
                f"New attribute value {new_value} must be between {self.min_value} and {self.max_value}."
            )
