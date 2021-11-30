import json

import attr
import cattr
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cyoa.models import Question, Choice, ChoiceResultType, Recommendation, Source
from cyoa.api import SendMailRequest, SendMailResponse
from cyoa.mail import send_mail

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

def check_game(request):
    game_state = game.GameState.from_current()
    generate_success = True
    try:
        _ = game.generate(game_state)
    except ValueError:
        generate_success = False
    
    traversal_success = True
    traversal_error = None
    try:
        traversal = game.traverse(game_state)
    except ValueError as e:
        traversal_success = False
        traversal_error = str(e)

    all_questions = Question.objects.all()
    root_questions = Question.objects.filter(root=True)

    questions_without_at_least_two_choices = {}
    questions_not_reachable = []
    for q in all_questions:
        choices = game_state.questions_to_choices.get(q.id, [])
        if len(choices) < 2:
            questions_without_at_least_two_choices[q.code] = [c.text for c in choices]
        
        if q.id not in traversal.questions:
            questions_not_reachable.append(q.code)
    
    choices_not_reachable = []
    choices_with_no_results = []
    choices_with_two_results = []
    choices_with_question_type_but_recommendation = []
    choices_with_recommendation_type_but_question = []
    for c in Choice.objects.all():
        if c.id not in traversal.choices:
            choices_not_reachable.append(c.text)
        
        if c.result_question is None and c.result_recommendation is None:
            choices_with_no_results.append(c.text)
        
        if not c.result_question is None and not c.result_recommendation is None:
            choices_with_two_results.append(c.text)
        
        if c.result_type == ChoiceResultType.QUESTION.value and not c.result_recommendation is None:
            choices_with_question_type_but_recommendation.append(c.text)
        
        if c.result_type == ChoiceResultType.RECOMMENDATION.value and not c.result_question is None:
            choices_with_recommendation_type_but_question.append(c.text)

    sources_not_reachable = []
    for s in Source.objects.all():
        if s.id not in traversal.sources:
            sources_not_reachable.append(s.name)
    
    recommendations_not_reachable = []
    for r in Recommendation.objects.all():
        if r.id not in traversal.recommendations:
            recommendations_not_reachable.append(r.title)
    
    
    context = {
        'generate_success': generate_success,
        'traversal_success': traversal_success,
        'traversal_error': traversal_error,
        'root_questions': root_questions,
        'exists_questions_without_at_least_two_choices': bool(questions_without_at_least_two_choices),
        'questions_without_at_least_two_choices': questions_without_at_least_two_choices,
        'questions_not_reachable': questions_not_reachable,
        'choices_not_reachable': choices_not_reachable,
        'sources_not_reachable': sources_not_reachable,
        'recommendations_not_reachable': recommendations_not_reachable,
        'choices_with_no_results': choices_with_no_results,
        'choices_with_two_results': choices_with_two_results,
        'choices_with_question_type_but_recommendation': choices_with_question_type_but_recommendation,
        'choices_with_recommendation_type_but_question': choices_with_recommendation_type_but_question,
    }
    return render(request, 'check.html', context=context)

@csrf_exempt # Frontend app will not have user session for CSRF token
def generate_lead(request):
    if request.method != 'POST':
        error_message = f"Invalid request method: {request.method}. Only POST is supported."
        return JsonResponse(attr.asdict(SendMailResponse(success=False, error_message=error_message)))
    
    post_data = json.loads(request.body)
    smr = cattr.structure(post_data, SendMailRequest)

    resp = send_mail(smr)
    if resp.status_code == 200:
        return JsonResponse(attr.asdict(SendMailResponse(success=True, error_message=None)))
    else:
        return JsonResponse(attr.asdict(SendMailResponse(success=False, error_message=resp.text)))