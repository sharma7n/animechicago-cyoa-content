from collections import defaultdict

import attr

from .models import Question, Source, Recommendation, Choice, ChoiceResultType


@attr.s
class GameState(object):
    root_question: Question = attr.ib()
    choices: "QuerySet" = attr.ib()
    questions_to_choices: defaultdict = attr.ib()
    
    @classmethod
    def from_question_and_choices(cls, root_question, choices):
        """ Generates an instance given a root question and choices set. """
        
        return cls(
            root_question=root_question,
            choices=choices,
            questions_to_choices=cls._generate_questions_to_choices(choices),
        )
    
    @classmethod
    def from_empty(cls):
        """ Generates an empty instance for testing. """
        
        return cls.from_question_and_choices(
            root_question=None,
            choices=cls._structure_choices().none(),
        )
    
    @classmethod
    def from_current(cls):
        """ Queries the database for the current game state. """
        
        return cls.from_question_and_choices(
            root_question=Question.objects.filter(root=True).first(),
            choices=cls._structure_choices().all(),
        )
    
    @classmethod
    def _structure_choices(cls) -> "QuerySet":
        """ Prepares a QuerySet for choices with all related data. """
        
        return (
            Choice
            .objects
            .select_related('question')
            .select_related('result_question')
            .select_related('result_recommendation')
        )
    
    @staticmethod
    def _generate_questions_to_choices(choices):
        """ Generate a map from each question to a list of its choices. """
        
        questions_to_choices = defaultdict(list)
        for choice in choices:
            questions_to_choices[choice.question.id].append(choice)
        return questions_to_choices
    
def generate(game_state: GameState) -> dict:
    """ Serializes the entire game state. """
    
    # Starting at the root question, recursively fill the data set
    def generate_question_data(question):
        valid_question = (
            question
            and (question.id in game_state.questions_to_choices)
        )
        
        if valid_question:
            return {
                'type': "Question",
                'text': question.text,
                'choices': [
                    {
                        'text': qc.text,
                        'result': generate_choice_data(qc),
                    }
                    for qc in game_state.questions_to_choices[question.id]
                ]
            }
        else:
            return {
                'type': "Error",
                'text': "Question node contains no data.",
            }
    
    def generate_choice_data(choice):
        return {
            ChoiceResultType.QUESTION.value: generate_question_data,
            ChoiceResultType.RECOMMENDATION.value: generate_recommendation_data,
        }.get(choice.result_type)(choice.result)
    
    def generate_recommendation_data(recommendation):
        return {
            'type': "Recommendation",
            'title': recommendation.title,
            'available_on': [
                {
                    'name': source.name,
                    'url': source.url,
                }
                for source in recommendation.available_on_iter()
            ]
        }
    
    if not game_state.root_question or not game_state.root_question.root:
        return {
            'type': "Error",
            'text': "Did not find a root question.",
        }
    else:
        return generate_question_data(game_state.root_question)

def get_leaves(node: dict) -> iter:
    """ Iterates through all of the game data and yields out the recommendations. """
    
    node_type = node['type']
    
    if node_type == "Error":
        raise ValueError(node['text'])
    elif node_type == "Recommendation":
        yield node
    elif node_type == "Question":
        for choice in node['choices']:
            yield from get_leaves(choice['result'])
    else:
        raise ValueError(f"Unknown node type {node_type}")

def get_paths(node: dict, path_parts: list=None) -> iter:
    """ Iterates through all of the game data and yields out each node along with its full path. """
    if not path_parts:
        path_parts = []
    
    def on_question():
        yield path_parts, f"Question: {node['text']}"
        for choice in node['choices']:
            yield from get_paths(choice['result'], path_parts + [choice['text'],])
    
    def on_recommendation():
        yield path_parts, f"Recommendation: {node['title']}"
    
    def on_error():
        yield path_parts, f"{node.get('type', 'Unknown')}: {node.get('text', 'no text attribute available')}"
    
    yield from {
        "Question": on_question,
        "Recommendation": on_recommendation,
    }.get(node['type'], on_error)()