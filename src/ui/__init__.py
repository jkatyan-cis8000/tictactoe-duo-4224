"""UI layer: terminal interface for Tic-Tac-Toe."""
import os
from src.runtime import TicTacToeGame
from src.types import Player


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_board(board: list[list[str]]) -> None:
    """Display the current board state."""
    print("\n   0   1   2")
    for row in range(3):
        print(f" {row} {board[row][0]} | {board[row][1]} | {board[row][2]}")
        if row < 2:
            print("  ---+---+---")
    print()


def get_player_input(current_player: Player) -> tuple[int, int]:
    """Get move input from the player."""
    while True:
        try:
            move = input(f"Player {current_player}, enter your move (row col): ").strip()
            parts = move.split()
            if len(parts) != 2:
                raise ValueError("Please enter two numbers separated by space")
            row, col = int(parts[0]), int(parts[1])
            if row < 0 or row > 2 or col < 0 or col > 2:
                raise ValueError("Row and column must be between 0 and 2")
            return row, col
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def display_result(game: TicTacToeGame) -> None:
    """Display the final game result."""
    result = game.check_result()
    clear_screen()
    display_board(game.board)

    if result.winner:
        print(f"\nPlayer {result.winner} wins!")
        print("Congratulations!")
    elif result.is_draw:
        print("\nIt's a draw!")
        print("Well played both players!")
    else:
        print("\nGame in progress...")


def play_again() -> bool:
    """Ask if players want to play again."""
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def main() -> None:
    """Main entry point for the CLI game."""
    game = TicTacToeGame()

    print("=" * 40)
    print("       TIC TAC TOE - DUAL PLAYER")
    print("=" * 40)
    print("\nInstructions:")
    print("- Enter row and column numbers (0-2)")
    print("- Example: '0 0' for top-left corner")
    print("- First to get 3 in a row wins!")
    print("=" * 40)

    while True:
        clear_screen()
        display_board(game.board)
        print(f"\nCurrent player: {game.current_player}")

        row, col = get_player_input(game.current_player)

        if not game.make_move(row, col):
            print("\nThat cell is already taken or invalid. Try again.")
            input("Press Enter to continue...")
            continue

        if game.is_game_over():
            clear_screen()
            display_board(game.board)
            display_result(game)
            if not play_again():
                break
            game.reset()
        else:
            input("Press Enter to switch players...")

    print("\nThanks for playing! Goodbye!")


if __name__ == "__main__":
    main()
