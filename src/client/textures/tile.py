from PIL import Image

from src.client.textures.texture import Texture
from src.common.logging import get_logger
from src.common.errors import InvalidTextureError


logger = get_logger("openbench_client")


class TileTexture(Texture):
    def __init__(self, texture_id: str, image: Image.Image):
        if image.size != (16, 16):
            logger.error(
                f"InvalidTextureError: Tile texture '{texture_id}' must be 16x16 pixels, but is {image.size}"
            )
            raise InvalidTextureError(
                f"Tile texture '{texture_id}' must be 16x16 pixels, but is {image.size}"
            )

        super().__init__(texture_id, image)
