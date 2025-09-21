from .entities.physics import Physics
from .entities.player import Player
from .entities.movement import PlayerMovement
from .entities.npe import NonPlayerEntity
from .entities.hitbox import Hitbox
from .atrribute import Attribute
from .world.tile import Tile
from .world.chunk import Chunk
from .world.set_tile import set_tile
from .camera import Camera
from .logging import get_logger
from .asset.pack_manager import PackManager
from .renderer.world import WorldRenderer
from .renderer.entities import EntityRenderer
from .settings.loader import load_settings
from .keybinds import KeybindManager

import pygame
import easygui
import sys
from uuid import uuid4


def show_game_panic_window(exc_type, exc_value, exc_traceback):
    error_message = f"An unrecoverable error occurred and the game crashed!\n\n{exc_type.__name__}: {exc_value}"
    try:
        easygui.buttonbox(error_message, "Game Panic!", choices=["OK"])
    except Exception as e:
        print(error_message)
        print(f"Failed to show panic window: {e}")

    sys.exit(1)


sys.excepthook = show_game_panic_window

logger = get_logger()

# Load settings
settings = load_settings()
logger.info(f"Settings loaded: {settings}")

# Default texture pack path
pack_manager = PackManager("assets/default")

# Create a simple world
chunks = []
for cx in range(3):
    tiles = [Tile(x, 15, "openbench.wood") for x in range(16)]
    chunk = Chunk((cx, 0), tiles)
    chunks.append(chunk)

# Create player
player = Player(uuid="player1", username="Player", position=(0, 10))

# Camera will follow player
camera = Camera(position=(0, 0), zoom=1.0)  # Start with default zoom

# Setup pygame
pygame.init()
pygame.display.set_caption("Openbench")

# Try to set custom cursor
cursor_surface = pack_manager.load_texture_as_surface("openbench.cursor")
cursor_data = None


def set_custom_cursor(zoom):
    global cursor_surface, cursor_data
    if cursor_surface:
        try:
            # Match cursor size to tile size at current zoom
            cursor_size = int(16 * zoom)
            cursor_size = max(8, min(cursor_size, 128))  # Clamp size
            cursor_surface_scaled = pygame.transform.scale(
                cursor_surface, (cursor_size, cursor_size)
            )
            cursor_data = pygame.cursors.Cursor((0, 0), cursor_surface_scaled)
            pygame.mouse.set_cursor(cursor_data)
        except Exception as e:
            logger.warning(f"Failed to set custom cursor: {e}")
    else:
        logger.info("Custom cursor 'openbench.cursor' not found, using default cursor.")


set_custom_cursor(camera.zoom)

icon = pack_manager.load_texture_as_surface("openbench.icon")
if icon:
    logger.info("Attempting to set icon... (may not work on some platforms)")
    pygame.display.set_icon(icon)

resolution = settings.get("resolution", (768, 768))

# Fullscreen setting
fullscreen = settings.get("fullscreen", False)
if fullscreen:
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(resolution)


# Renderer
renderer = WorldRenderer(pack_manager, screen)
entity_renderer = EntityRenderer(pack_manager, screen)

# List to hold spawned entities
spawned_entities = []

# FPS counter setup
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

keybind_manager = KeybindManager.from_settings(settings)
player_movement = PlayerMovement(player, keybind_manager)

# Preload click sound
click_sound = pack_manager.load_sound("openbench.click")

# Preload music sound and play it looping
music_sound = pack_manager.load_sound("openbench.music")
if music_sound:
    music_sound.set_volume(0.10)  # Set volume to 10%
    music_sound.play(loops=-1)

# --- Fixed timestep main loop ---

TICK_RATE = 60  # ticks per second
TICK_INTERVAL = 1.0 / TICK_RATE


mouse_left_held = False
mouse_right_held = False
last_tile_pos = None


def handle_events(running, camera):
    global mouse_left_held, mouse_right_held, last_tile_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            logger.info("Quit event received, exiting...")
            running[0] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x = camera.position[0] + mouse_x / camera.zoom
            world_y = camera.position[1] + mouse_y / camera.zoom
            tile_x = int(world_x // 16)
            tile_y = int(world_y // 16)
            last_tile_pos = (tile_x, tile_y)
            if event.button == 1:
                mouse_left_held = True
                if click_sound:
                    click_sound.play()
                set_tile(chunks, world_x, world_y, "openbench.wood")
            elif event.button == 3:
                mouse_right_held = True
                if click_sound:
                    click_sound.play()
                set_tile(chunks, world_x, world_y, None)
            elif event.button == 2:
                # Middle click: spawn entity
                entity_uuid = f"#{str(uuid4())}"
                hitbox = Hitbox(1.0, 1.0)
                attributes = {
                    "gravity": Attribute("gravity", 250.0),
                    "move_speed": Attribute("move_speed", 1.0),
                }
                entity = NonPlayerEntity(
                    uuid=entity_uuid,
                    texture_id="openbench.icon",
                    hitbox=hitbox,
                    position=(world_x, world_y),
                    attributes=attributes,
                )
                entity.physics = Physics(
                    entity, [tile for chunk in chunks for tile in chunk.tiles]
                )
                spawned_entities.append(entity)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_left_held = False
            elif event.button == 3:
                mouse_right_held = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x = camera.position[0] + mouse_x / camera.zoom
            world_y = camera.position[1] + mouse_y / camera.zoom
            tile_x = int(world_x // 16)
            tile_y = int(world_y // 16)
            if last_tile_pos != (tile_x, tile_y):
                if mouse_left_held:
                    set_tile(chunks, world_x, world_y, "openbench.wood")
                    last_tile_pos = (tile_x, tile_y)
                elif mouse_right_held:
                    set_tile(chunks, world_x, world_y, None)
                    last_tile_pos = (tile_x, tile_y)
        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x_before = camera.position[0] + mouse_x / camera.zoom
            world_y_before = camera.position[1] + mouse_y / camera.zoom
            zoom_factor = 1.1
            if event.y > 0:
                new_zoom = camera.zoom * zoom_factor
            elif event.y < 0:
                new_zoom = camera.zoom / zoom_factor
            else:
                new_zoom = camera.zoom
            new_zoom = max(0.5, min(new_zoom, 5.0))
            world_x_after = camera.position[0] + mouse_x / new_zoom
            world_y_after = camera.position[1] + mouse_y / new_zoom
            camera.position = (
                camera.position[0] + (world_x_before - world_x_after),
                camera.position[1] + (world_y_before - world_y_after),
            )
            camera.zoom = new_zoom
            set_custom_cursor(camera.zoom)


def update_game_logic(accumulated_time):
    keybind_manager.update()
    while accumulated_time[0] >= TICK_INTERVAL:
        player_movement.update()
        # Update spawned entities
        for entity in spawned_entities:
            dt = TICK_INTERVAL
            # Apply physics (gravity, collisions)
            entity.physics.world_tiles = [
                tile for chunk in chunks for tile in chunk.tiles
            ]
            entity.physics.apply(dt)
        accumulated_time[0] -= TICK_INTERVAL


def center_camera_on_player():
    hitbox = player.hitbox
    px, py = player.position
    if hitbox is not None:
        center_x = px + hitbox.center[0]
        center_y = py + hitbox.center[1]
    else:
        center_x = px
        center_y = py
    camera.position = (
        center_x - screen.get_width() / (2 * camera.zoom),
        center_y - screen.get_height() / (2 * camera.zoom),
    )


def fix_rendering_bug():
    player.position = (
        round(player.position[0] * 16) / 16,
        round(player.position[1] * 16) / 16,
    )


def render_frame():
    fix_rendering_bug()

    renderer.render_chunks(chunks, camera)
    entity_renderer.render_entities(spawned_entities, camera)

    pygame.display.flip()


def update_title(fps_stats: list[dict], player: Player):
    clock.tick()
    fps = clock.get_fps()
    now = pygame.time.get_ticks()
    fps_stats[0][now] = fps
    fps_stats[0] = {t: f for t, f in fps_stats[0].items() if now - t <= 1000}
    if not isinstance(fps_stats[0], dict):
        fps_stats[0] = {}
    fps_stats[0][now] = fps
    recent_fps = [f for t, f in fps_stats[0].items() if now - t <= 1000]
    avg_fps = sum(recent_fps) / len(recent_fps) if recent_fps else 0
    min_fps = min(recent_fps) if recent_fps else 0
    max_fps = max(recent_fps) if recent_fps else 0

    pygame.display.set_caption(
        f"Openbench - X {player.position[0] / 16} Y {player.position[1] / 16} - FPS {int(fps)} Avg {avg_fps:.1f} Min {min_fps:.1f} Max {max_fps:.1f}"
    )


running = [True]
fps_stats = [{}]
accumulated_time = [0.0]
last_time = pygame.time.get_ticks() / 1000.0  # seconds


try:
    while running[0]:
        current_time = pygame.time.get_ticks() / 1000.0
        frame_time = current_time - last_time
        last_time = current_time
        accumulated_time[0] += frame_time

        handle_events(running, camera)
        update_game_logic(accumulated_time)
        center_camera_on_player()
        render_frame()
        update_title(fps_stats, player)
except (KeyboardInterrupt, SystemExit):
    logger.info("Exiting game...")
except Exception as e:
    # Panic window will be shown by sys.excepthook
    raise
finally:
    pygame.quit()
