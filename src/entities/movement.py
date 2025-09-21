class PlayerMovement:
    def __init__(self, player, keybind_manager):
        self.player = player
        self.keybind_manager = keybind_manager

    def update(self):
        fly_speed = 8.0
        vx, vy = 0.0, 0.0
        if self.keybind_manager.is_active("left"):
            vx -= fly_speed
        if self.keybind_manager.is_active("right"):
            vx += fly_speed
        if self.keybind_manager.is_active("up"):
            vy -= fly_speed
        if self.keybind_manager.is_active("down"):
            vy += fly_speed
        self.player.velocity = [vx, vy]
        self.player.position = (
            self.player.position[0] + self.player.velocity[0],
            self.player.position[1] + self.player.velocity[1],
        )
        self.player.on_ground = False  # Disable ground checks in fly mode
