from src.enum.GameState import GameState


class GameContext:
    def __init__(self, screen, game_stats, game_state, difficulty, music_controller, reset_func):
        self.screen = screen
        self.game_stats = game_stats
        self.game_state = game_state
        self.difficulty = difficulty
        self.reset_func = reset_func
        self.music_controller = music_controller

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def is_game_over(self):
        if self.game_stats.get_hp <= 0:
            self.game_state = GameState.END_OVER

    def reset_game(self):
        self.reset_func()