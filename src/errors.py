class GameError(Exception):
    """Base exception for game errors."""

    pass


class InvalidChunkDataError(GameError):
    """Exception raised for invalid chunk data."""

    pass


class InvalidAssetError(GameError):
    """Exception raised for invalid asset."""

    pass


class InvalidEntityDataError(GameError):
    """Exception raised for invalid entity data."""

    pass


class InvalidPlayerDataError(GameError):
    """Exception raised for invalid player data."""

    pass


class InvalidNonPlayerEntityDataError(GameError):
    """Exception raised for invalid non-player entity data."""

    pass


class InvalidAttributeError(GameError):
    """Exception raised for invalid entity attributes."""

    pass


class InvalidCameraDataError(GameError):
    """Exception raised for invalid camera data."""

    pass


class InvalidHitboxDataError(GameError):
    """Exception raised for invalid hitbox data."""

    pass


class MissingTextureError(GameError):
    """Exception raised when a required texture is missing."""

    pass
