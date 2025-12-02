import json

from django.contrib import admin

from src.apps.core.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "game_over"]

    @admin.display()
    def formatted_board(self, obj):
        return json.dumps(obj.board, indent=2)
