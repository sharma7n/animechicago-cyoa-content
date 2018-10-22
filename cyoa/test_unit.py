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
                    drawer=1,
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
                    'drawer': 1,
                },
            },
        ],
    }

def test_get_recommendations_empty():
    with pytest.raises(KeyError):
        list(game.get_leaves({}))

def test_get_leaves():
    assert list("abc") == [rec['title'] for rec in game.get_leaves({
        'type': "Question",
        'choices': [
            {
                'result': {
                    'type': "Recommendation",
                    'title': "a",
                },
            },
            {
                'result': {
                    'type': "Question",
                    'choices': [
                        {
                            'result': {
                                'type': "Recommendation",
                                'title': "b",
                            },
                        },
                        {
                            'result': {
                                'type': "Recommendation",
                                'title': "c",
                            },
                        },
                    ],
                },
            },
        ],
    })]

def test_get_paths():
    assert list(game.get_paths({
        'type': "Question",
        'text': "Root",
        'choices': [
            {
                'text': "1",
                'result': {
                    'type': "Recommendation",
                    'title': "a",
                },
            },
            {
                'text': "2",
                'result': {
                    'type': "Question",
                    'text': "Branch",
                    'choices': [
                        {
                            'text': "3",
                            'result': {
                                'type': "Recommendation",
                                'title': "b"
                            },
                        },
                        {
                            'text': "4",
                            'result': {
                                'type': "Recommendation",
                                'title': "c"
                            },
                        },
                    ],
                },
            },
        ],
    })) == [
        ([], "Question: Root"),
        (list("1"), "Recommendation: a"),
        (list("2"), "Question: Branch"),
        (list("23"), "Recommendation: b"),
        (list("24"), "Recommendation: c"),
    ]