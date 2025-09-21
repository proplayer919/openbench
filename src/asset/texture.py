from pygame.surface import Surface
import pygame
from PIL import Image

from src.logging import get_logger
from src.errors import InvalidAssetError


logger = get_logger()


class Texture:
    def __init__(self, texture_id: str, image: Image.Image):
        self.texture_id = texture_id

        try:
            if not isinstance(image, Image.Image):
                logger.error(
                    f"InvalidAssetError: Provided image for texture '{texture_id}' is not a PIL Image object."
                )
                raise InvalidAssetError(
                    f"Invalid image type for texture '{texture_id}'."
                )

            if not hasattr(image, "size") or not hasattr(image, "mode"):
                logger.error(
                    f"InvalidAssetError: Image object for texture '{texture_id}' missing required attributes."
                )
                raise InvalidAssetError(
                    f"Image missing attributes for texture '{texture_id}'."
                )

            self.surface = Surface(image.size, pygame.SRCALPHA)
        except Exception as e:
            logger.exception(
                f"Failed to create Pygame Surface for texture '{texture_id}': {e}"
            )
            raise InvalidAssetError(
                f"Surface creation failed for texture '{texture_id}'."
            ) from e

        try:
            mode = "RGBA"  # Always use RGBA for transparency
            pygame_image = pygame.image.fromstring(image.tobytes(), image.size, mode)
            self.surface.blit(pygame_image, (0, 0))
        except Exception as e:
            logger.exception(
                f"Failed to blit image to surface for texture '{texture_id}': {e}"
            )
            raise InvalidAssetError(
                f"Blitting image failed for texture '{texture_id}'."
            ) from e

        try:
            self.width, self.height = image.size
        except Exception as e:
            logger.exception(
                f"Failed to get image size for texture '{texture_id}': {e}"
            )
            raise InvalidAssetError(
                f"Getting image size failed for texture '{texture_id}'."
            ) from e
