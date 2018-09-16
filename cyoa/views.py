from django.http import JsonResponse

from . import game
from . import urls


def get_game(request):
    game_state = game.GameState.from_current()
    data = game.generate(game_state)
    return JsonResponse(data)