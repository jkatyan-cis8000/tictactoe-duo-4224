"""Service layer: business logic for Tic-Tac-Toe."""
from src.types import BoardState, Player, Position, Move, GameResult, GameState
from src.config import BOARD_SIZE, EMPTY_CELL


def create_initial_board() -> list[list[str]]:
    """Create an empty 3x3 board."""
    return [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def create_initial_game_state(first_player: Player = "X") -> GameState:
    """Create the initial game state."""
    return GameState(
        board=create_initial_board(),
        current_player=first_player,
        moves=[]
    )


def is_valid_move(board: BoardState, row: int, col: int) -> bool:
    """Check if a move is valid (cell is empty and within bounds)."""
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False
    return board[row][col] == EMPTY_CELL


def apply_move(board: BoardState, row: int, col: int, player: Player) -> BoardState:
    """Apply a move to the board and return the new state."""
    new_board = [row.copy() for row in board]
    new_board[row][col] = player
    return new_board


def check_winner(board: BoardState) -> GameResult:
    """
    Check if there's a winner on the board.
    Returns GameResult with winner info or None if no winner.
    """
    # Check rows
    for row in range(BOARD_SIZE):
        if board[row][0] != EMPTY_CELL and all(board[row][0] == board[row][col] for col in range(BOARD_SIZE)):
            winning_positions = [(row, col) for col in range(BOARD_SIZE)]
            return GameResult(winner=board[row][0], is_draw=False, winning_positions=winning_positions)

    # Check columns
    for col in range(BOARD_SIZE):
        if board[0][col] != EMPTY_CELL and all(board[0][col] == board[row][col] for row in range(BOARD_SIZE)):
            winning_positions = [(row, col) for row in range(BOARD_SIZE)]
            return GameResult(winner=board[0][col], is_draw=False, winning_positions=winning_positions)

    # Check main diagonal
    if board[0][0] != EMPTY_CELL and all(board[0][0] == board[i][i] for i in range(BOARD_SIZE)):
        winning_positions = [(i, i) for i in range(BOARD_SIZE)]
        return GameResult(winner=board[0][0], is_draw=False, winning_positions=winning_positions)

    # Check anti-diagonal
    if board[0][BOARD_SIZE - 1] != EMPTY_CELL and all(board[0][BOARD_SIZE - 1] == board[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)):
        winning_positions = [(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)]
        return GameResult(winner=board[0][BOARD_SIZE - 1], is_draw=False, winning_positions=winning_positions)

    # Check for draw (full board)
    is_draw = all(board[row][col] != EMPTY_CELL for row in range(BOARD_SIZE) for col in range(BOARD_SIZE))

    return GameResult(winner=None, is_draw=is_draw, winning_positions=[])


def switch_player(player: Player) -> Player:
    """Switch to the other player."""
    return "O" if player == "X" else "X"


def make_move(game_state: GameState, row: int, col: int) -> GameState:
    """Apply a move to the game state and return the updated state."""
    if not is_valid_move(game_state.board, row, col):
        raise ValueError("Invalid move")

    new_board = apply_move(game_state.board, row, col, game_state.current_player)
    new_move = Move(player=game_state.current_player, row=row, col=col)
    new_moves = game_state.moves + [new_move]
    new_player = switch_player(game_state.current_player)

    return GameState(
        board=new_board,
        current_player=new_player,
        moves=new_moves
    )
