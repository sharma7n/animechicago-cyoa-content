from collections import defaultdict

from .models import Question, Source, Recommendation, Choice, ChoiceResultType


def generate() -> dict:
    """ Serializes the entire game state. """
    
    # Find the root question
    root_question = Question.objects.filter(root=True).first()
    
    # Find all choices with their related data
    choices = (
        Choice
        .objects
        .select_related('question')
        .select_related('result_question')
        .select_related('result_recommendation')
        .all()
    )
    
    # Find all recommendations
    recommendations = (
        Recommendation
        .objects
        .prefetch_related('available_on')
        .all()
    )
    
    # Build a map from questions to their choices
    questions_to_their_choices = defaultdict(list)
    for choice in choices:
        questions_to_their_choices[choice.question.id].append(choice)
    
    # Starting at the root question, recursively fill the data set
    
    def generate_question_data(question):
        return {
            'type': "Question",
            'text': question.text,
            'choices': [
                {
                    'text': qc.text,
                    'result': generate_choice_data(qc),
                }
                for qc in questions_to_their_choices[question.id]
            ]
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
                for source in recommendation.available_on.all()
            ]
        }
    
    return generate_question_data(root_question)