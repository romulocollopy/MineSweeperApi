from __future__ import annotations
from dataclasses import asdict
from django.db import models

from src.apps.core.domain.data_objects import Board, GameConfig, MineBlock


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def empty_board():
    return {"blocks": [[]]}


class GameManager(models.Manager):
    def new_game(
        self,
        slug: str,
        difficulty: GameConfig.Difficulty = GameConfig.Difficulty.medium,
    ):
        board = GameConfig(difficulty).new_board()
        return self.create(slug=slug, difficulty=difficulty, board=asdict(board))


class Game(BaseModel):
    objects = GameManager()

    slug = models.SlugField()
    board = models.JSONField(default=empty_board)
    game_over = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    finish_time = models.DateTimeField(null=True)
    difficulty = models.CharField(
        choices=[
            (d.name, "-".join(str(v) for v in d.value)) for d in GameConfig.Difficulty
        ]
    )

    def get_board(self):
        return Board(
            blocks=[[MineBlock(**b) for b in col] for col in self.board["blocks"]]
        )
