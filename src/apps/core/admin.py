import json

from django.contrib import admin
from django.utils.html import SafeString

from src.apps.core.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "slug", "game_over"]
    readonly_fields = ["formatted_board"]

    @admin.display()
    def formatted_board(self, obj):
        board = json.dumps(obj.board, indent=2)
        return SafeString(f"<pre>{board}</pre>")
