from enum import Enum

class GameState(Enum):
    MENU = 1
    RUNNING = 2
    PAUSED = 3
    END_OVER = 4
    WIN = 5
