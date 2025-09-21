import pygame


class KeybindManager:
    def __init__(self, keybinds: dict[str, list[int]]):
        """
        keybinds: dict mapping action names to lists of pygame key constants
        Example: {"move_left": [pygame.K_a, pygame.K_LEFT], "jump": [pygame.K_SPACE, pygame.K_UP]}
        """
        self.keybinds = keybinds
        self.active = set()

    def update(self):
        """Update active keys from pygame.key.get_pressed()"""
        pressed = pygame.key.get_pressed()
        self.active.clear()
        for action, keys in self.keybinds.items():
            if any(pressed[k] for k in keys):
                self.active.add(action)

    def is_active(self, action: str) -> bool:
        return action in self.active

    def get_active_actions(self) -> set:
        return set(self.active)

    @staticmethod
    def from_settings(settings: dict) -> "KeybindManager":
        """Create KeybindManager from settings dict (expects key names as strings)"""
        import pygame

        key_map = {
            "W": pygame.K_w,
            "A": pygame.K_a,
            "D": pygame.K_d,
            "S": pygame.K_s,
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
            "UP": pygame.K_UP,
            "DOWN": pygame.K_DOWN,
            "SPACE": pygame.K_SPACE,
        }
        keybinds = {}
        for action, keys in settings.get("keybinds", {}).items():
            keybinds[action] = [key_map[k] for k in keys if k in key_map]
        return KeybindManager(keybinds)
