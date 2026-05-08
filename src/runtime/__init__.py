"""Runtime layer: game loop orchestration."""
from src.service import make_move, check_winner, create_initial_game_state
from src.types import GameState, GameResult


class TicTacToeGame:
    """Manages the game state and flow."""

    def __init__(self):
        self._state = create_initial_game_state()

    @property
    def current_player(self) -> str:
        """Get the current player."""
        return self._state.current_player

    @property
    def board(self) -> list[list[str]]:
        """Get the current board state."""
        return self._state.board

    @property
    def moves(self) -> list:
        """Get the list of moves made."""
        return self._state.moves

    def is_game_over(self) -> bool:
        """Check if the game has ended."""
        result = self.check_result()
        return result.winner is not None or result.is_draw

    def check_result(self) -> GameResult:
        """Check if there's a winner or draw."""
        return check_winner(self._state.board)

    def make_move(self, row: int, col: int) -> bool:
        """
        Attempt to make a move.
        Returns True if the move was valid and applied, False otherwise.
        """
        from src.service import is_valid_move
        if not is_valid_move(self._state.board, row, col):
            return False

        self._state = make_move(self._state, row, col)
        return True

    def reset(self) -> None:
        """Reset the game to its initial state."""
        self._state = create_initial_game_state()
