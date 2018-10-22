from pprint import pprint

import pytest

from . import game
from . import models

@pytest.mark.django_db
def test_game_generate_complex():
    
    # --- Setup Sources
    
    vrv = models.Source(
        name="VRV",
        url="https://vrv.co",
    )
    vrv.save()
    
    funimation = models.Source(
        name="Funimation",
        url="https://funimation.com",
    )
    funimation.save()
    
    # --- Setup Questions
    
    root_question = models.Question(
        root=True,
        text="What genre do you like?",
    )
    root_question.save()
    
    action_question = models.Question(
        root=False,
        text="What's your favorite kind of weapon?",
    )
    action_question.save()
    
    comedy_question = models.Question(
        root=False,
        text="What kind of setting would you prefer?",
    )
    comedy_question.save()
    
    theme_question = models.Question(
        root=False,
        text="Do you prefer light-hearted or tragic stories?",
    )
    theme_question.save()
    
    # --- Setup Recommendations
    
    killlakill = models.Recommendation(
        title="Kill La Kill",
        drawer=1,
    )
    killlakill.save()
    killlakill.available_on.add(funimation)
    
    berserk = models.Recommendation(
        title="Berserk",
        drawer=2,
    )
    berserk.save()
    berserk.available_on.add(funimation)
    
    ippo = models.Recommendation(
        title="Hajime no Ippo",
        drawer=2,
    )
    ippo.save()
    ippo.available_on.add(vrv)
    
    mobpsycho = models.Recommendation(
        title="Mob Psycho 100",
        drawer=3,
    )
    mobpsycho.save()
    mobpsycho.available_on.add(funimation)
    mobpsycho.available_on.add(vrv)
    
    tonegawa = models.Recommendation(
        title="Mr. Tonegawa Middle Management Blues",
        drawer=4,
    )
    tonegawa.save()
    tonegawa.available_on.add(vrv)
    
    # --- Setup Choices
    
    choices = [
        models.Choice(
            question=root_question,
            text="Action",
            result_type="Question",
            result_question=action_question,
        ),
        models.Choice(
            question=root_question,
            text="Comedy",
            result_type="Question",
            result_question=comedy_question,
        ),
        models.Choice(
            question=action_question,
            text="Sword",
            result_type="Question",
            result_question=theme_question,
        ),
        models.Choice(
            question=action_question,
            text="Fist",
            result_type="Recommendation",
            result_recommendation=ippo,
        ),
        models.Choice(
            question=comedy_question,
            text="School",
            result_type="Recommendation",
            result_recommendation=mobpsycho,
        ),
        models.Choice(
            question=comedy_question,
            text="Office",
            result_type="Recommendation",
            result_recommendation=tonegawa,
        ),
        models.Choice(
            question=theme_question,
            text="Light-Hearted",
            result_type="Recommendation",
            result_recommendation=killlakill,
        ),
        models.Choice(
            question=theme_question,
            text="Tragic",
            result_type="Recommendation",
            result_recommendation=berserk,
        ),
    ]
    
    for choice in choices:
        choice.save()
    
    # --- Perform the test
    state = game.GameState.from_current()
    result = game.generate(state)
    
    expected = {
        'type': "Question",
        'text': "What genre do you like?",
        'choices': [
            {
                'text': "Action",
                'result': {
                    'type': "Question",
                    'text': "What's your favorite kind of weapon?",
                    'choices': [
                        {
                            'text': "Sword",
                            'result': {
                                'type': "Question",
                                'text': "Do you prefer light-hearted or tragic stories?",
                                'choices': [
                                    {
                                        'text': "Light-Hearted",
                                        'result': {
                                            'type': "Recommendation",
                                            'title': "Kill La Kill",
                                            'available_on': [
                                                {
                                                    'name': "Funimation",
                                                    'url': "https://funimation.com",
                                                },
                                            ],
                                            'drawer': 1,
                                        },
                                    },
                                    {
                                        'text': "Tragic",
                                        'result': {
                                            'type': "Recommendation",
                                            'title': "Berserk",
                                            'available_on': [
                                                {
                                                    'name': "Funimation",
                                                    'url': "https://funimation.com",
                                                },
                                            ],
                                            'drawer': 2,
                                        },
                                    },
                                ],
                            },
                        },
                        {
                            'text': "Fist",
                            'result': {
                                'type': "Recommendation",
                                'title': "Hajime no Ippo",
                                'available_on': [
                                    {
                                        'name': "VRV",
                                        'url': "https://vrv.co",
                                    },
                                ],
                                'drawer': 2,
                            },
                        },
                    ],
                },
            },
            {
                'text': "Comedy",
                'result': {
                    'type': "Question",
                    'text': "What kind of setting would you prefer?",
                    'choices': [
                        {
                            'text': "School",
                            'result': {
                                'type': "Recommendation",
                                'title': "Mob Psycho 100",
                                'available_on': [
                                    {
                                        'name': "VRV",
                                        'url': "https://vrv.co",
                                    },
                                    {
                                        'name': "Funimation",
                                        'url': "https://funimation.com",
                                    },
                                ],
                                'drawer': 3,
                            },
                        },
                        {
                            'text': "Office",
                            'result': {
                                'type': "Recommendation",
                                'title': "Mr. Tonegawa Middle Management Blues",
                                'available_on': [
                                    {
                                        'name': "VRV",
                                        'url': "https://vrv.co",
                                    },
                                ],
                                'drawer': 4,
                            },
                        },
                    ],    
                },
            },
        ],
    }
    
    assert result == expected