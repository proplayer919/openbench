import os
from PIL import Image
from pygame import Surface
import pygame


class TexturePack:
    def __init__(self, pack_dir):
        self.pack_dir = pack_dir
        self._texture_cache = {}
        self._surface_cache = {}

    def get_texture_path(self, texture_id):
        return os.path.join(self.pack_dir, f"{texture_id}.png")

    def has_texture(self, texture_id):
        return os.path.isfile(self.get_texture_path(texture_id))

    def load_texture(self, texture_id):
        if texture_id in self._texture_cache:
            return self._texture_cache[texture_id]
        path = self.get_texture_path(texture_id)
        if os.path.isfile(path):
            img = Image.open(path).convert("RGBA")  # Ensure RGBA for transparency
            self._texture_cache[texture_id] = img
            return img
        return None

    def load_texture_as_surface(self, texture_id):
        if texture_id in self._surface_cache:
            return self._surface_cache[texture_id]
        img = self.load_texture(texture_id)
        if img:
            mode = "RGBA"  # Always use RGBA for transparency
            surface = Surface(img.size, pygame.SRCALPHA)
            pygame_image = pygame.image.fromstring(img.tobytes(), img.size, mode)
            surface.blit(pygame_image, (0, 0))
            self._surface_cache[texture_id] = surface
            return surface
        return None


class PackManager:
    def __init__(self, default_pack_dir, custom_pack_dir=None):
        self.default_pack = TexturePack(default_pack_dir)
        self.custom_pack = TexturePack(custom_pack_dir) if custom_pack_dir else None

    def load_texture(self, texture_id):
        if self.custom_pack and self.custom_pack.has_texture(texture_id):
            return self.custom_pack.load_texture(texture_id)

        if self.default_pack.has_texture(texture_id):
            return self.default_pack.load_texture(texture_id)

        if self.default_pack.has_texture("openbench.missing"):
            return self.default_pack.load_texture("openbench.missing")

        return None

    def load_texture_as_surface(self, texture_id):
        if self.custom_pack and self.custom_pack.has_texture(texture_id):
            return self.custom_pack.load_texture_as_surface(texture_id)

        if self.default_pack.has_texture(texture_id):
            return self.default_pack.load_texture_as_surface(texture_id)

        if self.default_pack.has_texture("openbench.missing"):
            return self.default_pack.load_texture_as_surface("openbench.missing")

        return None
