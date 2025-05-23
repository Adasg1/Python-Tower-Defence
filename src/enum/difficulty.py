from enum import Enum

class Difficulty(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"

    def __str__(self):
        return self.value