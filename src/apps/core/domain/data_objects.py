from __future__ import annotations
from itertools import chain
import math
import random

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Self

from .exceptions import Boom


@dataclass
class Coordinates:
    x: int
    y: int


@dataclass
class MineBlock:
    """Represents a single block on the minesweeper board"""

    coordinates: Coordinates
    is_bomb: bool = False
    display: str = ""

    def dig(self, board: Board, origin: Self | None = None) -> Board:
        self.reveal(board)

        if self.is_bomb:
            raise Boom("Good try!", board)

        if self.bombs_around(board) == 0:
            for neighbor in self.get_neighbors(board):
                if origin and neighbor.coordinates == origin.coordinates:
                    continue
                neighbor.dig(board, self)

        return board

    def reveal(self, board: Board) -> None:
        if self.is_bomb:
            self.display = "💣"
        else:
            self.display = str(self.bombs_around(board))

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
        return asdict(self)


@dataclass
class Board:
    blocks: list[list[MineBlock]]

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
        blocks = [asdict(b) for b in chain(*self.blocks)]
        return {**asdict(self), "blocks": blocks}


@dataclass
class GameConfig:
    """Configuration for game settings"""

    class Difficulty(Enum):
        easy = (10, 10, 1)
        medium = (16, 16, 40)
        hard = (20, 20, 100)

    difficulty: Difficulty

    def new_board(self):
        return Board(blocks=generate_blocks(*self.difficulty.value))


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
