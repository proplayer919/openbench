import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.common.world.tile import Tile
from src.common.world.chunk import Chunk
from src.common.camera import Camera
from src.common.logging import get_logger
from src.client.asset.pack_manager import PackManager
from src.client.renderer.world import WorldRenderer
from src.client.settings.loader import load_settings

import pygame

logger = get_logger("openbench_client")

# Load settings
settings = load_settings()
logger.info(f"Settings loaded: {settings}")

# Default texture pack path
pack_manager = PackManager("assets/default")

# Create a simple chunk
chunks = []
for cx in range(3):
    for cy in range(3):
        tiles = [Tile(x, y, "openbench.car") for x in range(16) for y in range(16)]
        chunk = Chunk((cx, cy), tiles)
        chunks.append(chunk)

# Camera centered at (0, 0), zoom 1.0
camera = Camera(position=(0, 0), zoom=settings.get("zoom", 1.0))

# Setup pygame
pygame.init()
pygame.display.set_caption("Openbench")

# Try to set custom cursor
cursor_surface = pack_manager.load_texture_as_surface("openbench.cursor")
cursor_data = None
if cursor_surface:
    try:
        cursor_surface = pygame.transform.scale(cursor_surface, (32, 32))
        cursor_data = pygame.cursors.Cursor((0, 0), cursor_surface)
        pygame.mouse.set_cursor(cursor_data)
        logger.info("Custom cursor set from texture 'openbench.cursor'.")
    except Exception as e:
        logger.warning(f"Failed to set custom cursor: {e}")
else:
    logger.info("Custom cursor 'openbench.cursor' not found, using default cursor.")

icon = pack_manager.load_texture_as_surface("openbench.icon")
if icon:
    logger.info("Attempting to set icon... (may not work on some platforms)")
    pygame.display.set_icon(icon)

resolution = settings.get("resolution", (300, 300))

vsync = settings.get("vsync", True)
screen = pygame.display.set_mode(resolution, vsync=1 if vsync else 0)

# Renderer
renderer = WorldRenderer(pack_manager, screen)

# FPS counter setup
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Main loop

# Preload click sound
click_sound = pack_manager.load_sound("openbench.click")

# Preload music sound and play it looping
music_sound = pack_manager.load_sound("openbench.music")
if music_sound:
    music_sound.play(loops=-1)

running = True
while running:
    renderer.render_chunks(chunks, camera)

    max_fps = settings.get("max_fps")
    if max_fps:
        clock.tick(max_fps)
    else:
        clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logger.info("Quit event received, exiting...")
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_sound:
                click_sound.play()
pygame.quit()
sys.exit(0)
