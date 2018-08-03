import enum

from django.db import models

class Question(models.Model):
    """ A question with one or more possible answers. """
    
    root = models.BooleanField(default=False)
    text = models.TextField()

class Source(models.Model):
    """ A place where the recommendation can be accessed or obtained. """
    
    name = models.CharField(max_length=128)
    url = models.URLField()

class Recommendation(models.Model):
    """ A media item recommended by the app. """
    
    title = models.CharField(max_length=256)
    description = models.TextField()
    available_on = models.ManyToManyField(Source)

class ChoiceResultType(enum.Enum):
    """ Possible result types for a Choice. """
    
    QUESTION = "Question"
    RECOMMENDATION = "Recommendation"

class Choice(models.Model):
    """ Question answer that may lead to another question or a recommendation. """
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="question",
    )
    
    text = models.CharField(max_length=256)
    
    result_type = models.CharField(
        max_length=max(len(item.value) for item in ChoiceResultType),
        choices=[(item, item.value) for item in ChoiceResultType],
        default=ChoiceResultType.QUESTION,
    )
    
    result_question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        blank=True,
        related_name="result_question",
    )
    
    result_recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.PROTECT,
        blank=True,
        related_name="result_recommendation",
    )