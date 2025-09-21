from src.errors import InvalidCameraDataError
from src.logging import get_logger

logger = get_logger("openbench_common")


class Camera:
    def __init__(self, position=(0, 0), orientation=0, zoom=1.0):
        if not (isinstance(position, tuple) and len(position) == 2):
            logger.error("InvalidCameraDataError: Invalid position data: %s", position)
            raise InvalidCameraDataError("Position must be a tuple of 2 elements.")

        if not (isinstance(orientation, (int, float))):
            logger.error(
                "InvalidCameraDataError: Invalid orientation data: %s", orientation
            )
            raise InvalidCameraDataError(
                "Orientation must be a number (angle in degrees)."
            )

        if not (isinstance(zoom, (int, float)) and zoom > 0):
            logger.error("InvalidCameraDataError: Invalid zoom value: %s", zoom)
            raise InvalidCameraDataError("Zoom must be a positive number.")

        self.position = position
        self.orientation = orientation  # angle in degrees
        self.zoom = zoom

    def move(self, dx, dy):
        try:
            x, y = self.position
            self.position = (x + dx, y + dy)
        except Exception as e:
            logger.exception("Error moving camera: %s", e)
            raise InvalidCameraDataError("Failed to move camera.")

    def rotate(self, dangle):
        try:
            self.orientation += dangle
        except Exception as e:
            logger.exception("Error rotating camera: %s", e)
            raise InvalidCameraDataError("Failed to rotate camera.")

    def set_zoom(self, zoom):
        if not (isinstance(zoom, (int, float)) and zoom > 0):
            logger.error("InvalidCameraDataError: Invalid zoom value: %s", zoom)
            raise InvalidCameraDataError("Zoom must be a positive number.")
        self.zoom = zoom
