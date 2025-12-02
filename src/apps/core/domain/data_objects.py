from __future__ import annotations
from itertools import chain
import math
import random

from dataclasses import asdict, dataclass
from enum import Enum, StrEnum

from src.apps.core.domain.exceptions import Boom


class Symbols(StrEnum):
    empty = "-"
    flag = "🚩"
    bomb = "💣"


@dataclass
class Coordinates:
    x: int
    y: int


@dataclass
class MineBlock:
    """Represents a single block on the minesweeper board"""

    coordinates: Coordinates
    is_bomb: bool = False
    is_flagged: bool = False
    display: str = ""

    def __post_init__(self):
        if isinstance(self.coordinates, dict):
            self.coordinates = Coordinates(**self.coordinates)

    def dig(self, board: Board, visited: set[tuple[int, int]] | None = None) -> Board:
        if visited is None:
            visited = set()

        coord_tuple = (self.coordinates.x, self.coordinates.y)
        if coord_tuple in visited:
            return board  # Already revealed

        visited.add(coord_tuple)
        self.reveal(board)

        if self.is_bomb:
            raise Boom("Good try!", board)

        if self.bombs_around(board) == 0:
            for neighbor in self.get_neighbors(board):
                neighbor.dig(board, visited)

        return board

    def flag(self, board):
        if board.get_flag():
            self.is_flagged = True
            self.display = Symbols.flag

    def remove_flag(self, board):
        if self.is_flagged:
            self.is_flagged = False
            self.display = ""
            board.return_flag()

    def reveal(self, board: Board) -> None:
        if self.is_bomb:
            self.display = Symbols.bomb
            return

        if bombs := self.bombs_around(board):
            self.display = str(bombs)
            return

        self.display = Symbols.empty

    def get_neighbors(self, board: Board) -> list[MineBlock]:
        x = self.coordinates.x
        y = self.coordinates.y

        # The 8 possible neighbor offsets
        deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        neighbors = []
        for dx, dy in deltas:
            coord = Coordinates(x + dx, y + dy)

            try:
                n = board.get_block(coord)
            except ValueError:
                pass
            else:
                neighbors.append(n)

        return neighbors

    def bombs_around(self, board: Board) -> int:
        neighbors = self.get_neighbors(board)
        return len([n for n in neighbors if n.is_bomb])

    def as_dict(self):
        api_dict = asdict(self)
        del api_dict["is_bomb"]
        return api_dict


@dataclass
class Board:
    blocks: list[list[MineBlock]]
    flags: int
    slug: str = ""

    def get_block(self, coordinates: Coordinates) -> MineBlock:
        """Get a block at specific coordinates"""
        if coordinates.x < 0 or coordinates.y < 0:
            raise ValueError(f"coordinates can't be negative: {coordinates}")

        try:
            return self.blocks[coordinates.x][coordinates.y]
        except IndexError:
            raise ValueError(f"Invalid coordinates for board: {coordinates}")

    def replace_block(self, new_block: MineBlock) -> None:
        """Replace a block on the board"""
        x, y = (new_block.coordinates.x, new_block.coordinates.y)
        self.blocks[x][y] = new_block

    @property
    def grid_size(self) -> tuple[int, int]:
        """Calculate the grid size based on block coordinates"""

        width = len(self.blocks)
        height = len(self.blocks) if width else 0
        return (width, height)

    def as_dict(self):
        blocks = [bl.as_dict() for bl in chain(*self.blocks)]
        return {**asdict(self), "blocks": blocks}

    def get_flag(self):
        if self.flags > 0:
            self.flags -= 1
            return True
        return False

    def return_flag(self):
        self.flags += 1


@dataclass
class GameConfig:
    """Configuration for game settings"""

    class Difficulty(Enum):
        easy = (10, 10, 1)
        medium = (16, 16, 40)
        hard = (20, 20, 100)

    difficulty: Difficulty

    def new_board(self, slug=""):
        width, height, bombs = self.difficulty.value
        return Board(
            blocks=generate_blocks(width, height, bombs), flags=bombs, slug=slug
        )


def generate_blocks(width: int, height: int, bomb_count: int) -> list[list[MineBlock]]:
    total_blocks = width * height

    if bomb_count > total_blocks:
        raise ValueError("Bomb count cannot exceed total number of blocks")

    blocks_row = []
    for x in range(width):
        blocks_row.append(
            [
                MineBlock(coordinates=Coordinates(x, y), is_bomb=False)
                for y in range(height)
            ]
        )

    bomb_indexes = set()
    while len(bomb_indexes) < bomb_count:
        bomb_indexes.add(math.floor(random.random() * total_blocks))

    for index in bomb_indexes:
        list(chain(*blocks_row))[index].is_bomb = True

    return blocks_row
