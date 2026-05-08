# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- `src/types/__init__.py`: Pure type definitions (Player, BoardState, Move, GameResult, GameState)
- `src/config/__init__.py`: Configuration constants (BOARD_SIZE, EMPTY_CELL)
- `src/service/__init__.py`: Business logic (valid move checking, win detection, move application)
- `src/runtime/__init__.py`: Game orchestration (TicTacToeGame class managing state)
- `src/ui/__init__.py`: CLI interface (display, input handling, main game loop)
- `src/utils/__init__.py`: Pure helper functions (none currently needed)
- `src/providers/__init__.py`: Cross-cutting concerns (none currently needed)

## Interfaces

### Type Exports (`src/types/__init__.py`)
- `Player = Literal["X", "O"]`: Player identifier
- `Position = tuple[int, int]`: Board position (row, col)
- `BoardState = list[list[Optional[Player]]]`: Current board state
- `Move(player: Player, row: int, col: int)`: A player's move
- `GameResult(winner: Optional[Player], is_draw: bool, winning_positions: list[Position])`: Game outcome
- `GameState(board: BoardState, current_player: Player, moves: list[Move])`: Full game state

### Service Exports (`src/service/__init__.py`)
- `create_initial_board() -> BoardState`: Create empty 3x3 board
- `create_initial_game_state(first_player: Player = "X") -> GameState`: Initial game state
- `is_valid_move(board, row, col) -> bool`: Check if move is valid
- `apply_move(board, row, col, player) -> BoardState`: Apply move to board
- `check_winner(board) -> GameResult`: Check for winner or draw
- `switch_player(player) -> Player`: Switch to other player
- `make_move(game_state, row, col) -> GameState`: Apply move to game state

### Runtime Exports (`src/runtime/__init__.py`)
- `TicTacToeGame` class:
  - `__init__()`: Initialize game with empty board
  - `current_player: str`: Get current player
  - `board: BoardState`: Get board state
  - `is_game_over() -> bool`: Check if game ended
  - `check_result() -> GameResult`: Get winner/draw status
  - `make_move(row, col) -> bool`: Attempt move, returns success
  - `reset() -> None`: Reset to initial state

### UI Exports (`src/ui/__init__.py`)
- `main() -> None`: Entry point for CLI game
- `display_board(board)`: Render board to terminal
- `get_player_input(player) -> (int, int)`: Get move from player
- `display_result(game)`: Show game outcome

## Shared Data Structures

- Board is represented as a 3x3 list of lists with "X", "O", or " " (EMPTY_CELL)
- Moves are validated before application to ensure they land on empty cells
- Game result includes winner (if any), draw status, and winning positions

## External Dependencies

- No external dependencies required. Uses only Python standard library.
