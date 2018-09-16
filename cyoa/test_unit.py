import pytest

from . import game
from . import types


def test_game_generate_empty():
    state = game.GameState.from_empty()
    result = game.generate(state)
    assert result['type'] == "Error"

def test_game_generate_single_root_question_no_choices():
    state = game.GameState.from_question_and_choices(
        root_question=types.Question(root=True, text="Root"),
        choices=[],
    )
    
    result = game.generate(state)
    
    assert result['type'] == "Error"

def test_game_generate_single_nonroot_question_with_choices():
    nonroot_question = types.Question(root=False, text="Non-Root")
    
    recommendation = types.Recommendation(
        title="Recommendation",
        available_on=[
            types.Source(name="Source", url="https://source.com")
        ],
    )
    
    state = game.GameState.from_question_and_choices(
        root_question=nonroot_question,
        choices=[
            types.Choice(
                question=nonroot_question,
                text="Choice",
                result_type="Question",
                result_recommendation=recommendation,
            ),
        ],
    )
    result = game.generate(state)
    
    assert result['type'] == "Error"

def test_one_choice_quiz():
    root_question = types.Question(root=True, text="Root")
    state = game.GameState.from_question_and_choices(
        root_question=root_question,
        choices=[
            types.Choice(
                question=root_question,
                text="Choice",
                result_type="Recommendation",
                result_recommendation=types.Recommendation(
                    title="Recommendation",
                    available_on=[
                        types.Source(
                            name="Source", 
                            url="https://source.com"
                        ),
                    ],
                ),
            ),
        ],
    )
    result = game.generate(state)
    
    assert result == {
        'type': "Question",
        'text': "Root",
        'choices': [
            {
                'text': "Choice",
                'result': {
                    'type': "Recommendation",
                    'title': "Recommendation",
                    'available_on': [
                        {
                            'name': "Source",
                            'url': "https://source.com",
                        },
                    ],
                },
            },
        ],
    }