import enum

from django.db import models

class Question(models.Model):
    """ A question with one or more possible answers. """
    
    root = models.BooleanField(default=False)
    code = models.SlugField(null=True, blank=True)
    text = models.TextField()
    
    def __str__(self):
        return (
            f"{'ROOT - ' if self.root else ''}"
            f"{self.code} - {self.text}"
        )

class Source(models.Model):
    """ A place where the recommendation can be accessed or obtained. """
    
    name = models.CharField(max_length=128)
    url = models.URLField()
    
    def __str__(self):
        return f"{self.name}"

class Recommendation(models.Model):
    """ A media item recommended by the app. """
    
    title = models.CharField(max_length=256)
    available_on = models.ManyToManyField(Source)
    drawer = models.PositiveSmallIntegerField(null=True, blank=True)
    
    def available_on_iter(self):
        return self.available_on.all()
    
    def __str__(self):
        return f"{self.title}"

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
        choices=[(item.value, item.value) for item in ChoiceResultType],
        default=ChoiceResultType.QUESTION,
    )
    
    result_question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="result_question",
    )
    
    result_recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="result_recommendation",
    )
    
    @property
    def result(self):
        return {
            ChoiceResultType.QUESTION.value: self.result_question,
            ChoiceResultType.RECOMMENDATION.value: self.result_recommendation,
        }.get(self.result_type)
    
    def __str__(self):
        return (
            f"{self.question} "
            f"{self.text}"
        )