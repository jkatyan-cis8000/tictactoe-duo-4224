"""Pure type definitions for the Tic-Tac-Toe game."""
from dataclasses import dataclass
from typing import Literal, Optional

Player = Literal["X", "O"]
Position = tuple[int, int]
BoardState = list[list[Optional[Player]]]


@dataclass
class Move:
    """A player's move on the board."""
    player: Player
    row: int
    col: int


@dataclass
class GameResult:
    """The result of a game."""
    winner: Optional[Player]
    is_draw: bool
    winning_positions: list[Position]


@dataclass
class GameState:
    """Current state of the game."""
    board: BoardState
    current_player: Player
    moves: list[Move]
