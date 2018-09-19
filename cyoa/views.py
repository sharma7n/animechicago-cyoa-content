from django.http import JsonResponse
from django.shortcuts import render

from . import game
from . import urls


def get_game(request):
    game_state = game.GameState.from_current()
    data = game.generate(game_state)
    return JsonResponse(data)

def view_game(request):
    game_state = game.GameState.from_current()
    try:
        data = game.generate(game_state)
    except ValueError:
        data = {}
    
    paths = game.get_paths(data)
    readable_paths = [
        (" > ".join(path), result)
        for path, result in paths
    ]
    context = {'readable_paths': readable_paths}
    return render(request, 'paths.html', context=context)