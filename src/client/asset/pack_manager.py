import os
from PIL import Image
from pygame import Surface
import pygame
import pygame.mixer


class AssetPack:
    def __init__(self, pack_dir):
        self.pack_dir = pack_dir
        self._texture_cache = {}
        self._surface_cache = {}
        self._sound_cache = {}

    def get_texture_path(self, texture_id):
        return os.path.join(self.pack_dir, "textures", f"{texture_id}.png")

    def get_sound_path(self, sound_id):
        return os.path.join(self.pack_dir, "sounds", f"{sound_id}.wav")

    def has_texture(self, texture_id):
        return os.path.isfile(self.get_texture_path(texture_id))

    def has_sound(self, sound_id):
        return os.path.isfile(self.get_sound_path(sound_id))

    def load_texture(self, texture_id):
        if texture_id in self._texture_cache:
            return self._texture_cache[texture_id]
        path = self.get_texture_path(texture_id)
        if os.path.isfile(path):
            img = Image.open(path).convert("RGBA")
            self._texture_cache[texture_id] = img
            return img
        return None

    def load_texture_as_surface(self, texture_id):
        if texture_id in self._surface_cache:
            return self._surface_cache[texture_id]
        img = self.load_texture(texture_id)
        if img:
            mode = "RGBA"
            surface = Surface(img.size, pygame.SRCALPHA)
            pygame_image = pygame.image.fromstring(img.tobytes(), img.size, mode)
            surface.blit(pygame_image, (0, 0))
            self._surface_cache[texture_id] = surface
            return surface
        return None

    def load_sound(self, sound_id):
        if sound_id in self._sound_cache:
            return self._sound_cache[sound_id]
        path = self.get_sound_path(sound_id)
        if os.path.isfile(path):
            sound = pygame.mixer.Sound(path)
            self._sound_cache[sound_id] = sound
            return sound
        return None


class PackManager:
    def __init__(self, default_pack_dir, custom_pack_dir=None):
        self.default_pack = AssetPack(default_pack_dir)
        self.custom_pack = AssetPack(custom_pack_dir) if custom_pack_dir else None

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

    def load_sound(self, sound_id):
        if self.custom_pack and self.custom_pack.has_sound(sound_id):
            return self.custom_pack.load_sound(sound_id)
        if self.default_pack.has_sound(sound_id):
            return self.default_pack.load_sound(sound_id)
        return None
