from Game import Game
from Enum.GameState import GameState


def main():
    game = Game()

    while True:
        match game.game_state:
            case GameState.MENU:
                game.menu()
            case GameState.RUNNING:
                game.run()
            case GameState.PAUSED:
                game.pause()
            case GameState.GAME_OVER:
                game.game_over()

if __name__ == '__main__':
    main()









