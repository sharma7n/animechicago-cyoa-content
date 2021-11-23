from django.core.management.base import BaseCommand, CommandError

from cyoa.models import Question, Choice, Recommendation, Source, ChoiceResultType

class Command(BaseCommand):
    help = 'Creates sample records in the database'

    def handle(self, *args, **options):
        q1 = Question(
            root=True,
            code="COMEDY_OR_DRAMA",
            text="Do you prefer comedy or drama?",
        )
        q1.save()

        q2 = Question(
            root=False,
            code="COMEDY_TYPE",
            text="Do you prefer action or romance?",
        )
        q2.save()

        s1 = Source(
            name="Crunchyroll",
            url="https://crunchyroll.com",
        )
        s1.save()

        r1 = Recommendation(
            title="Hajime no Ippo",
            drawer=0,
        )
        r1.save()
        r1.available_on.set([s1])
        r1.save()
        

        r2 = Recommendation(
            title="Toradora",
            drawer=0,
        )
        r2.save()
        r2.available_on.set([s1])
        r2.save()

        r3 = Recommendation(
            title="Vinland Saga",
            drawer=0,
        )
        r3.save()
        r3.available_on.set([s1])
        r3.save()

        c1 = Choice(
            question=q1,
            text="Comedy",
            result_type=ChoiceResultType.QUESTION.value,
            result_question=q2,
        )
        c1.save()

        c2 = Choice(
            question=q1,
            text="Drama",
            result_type=ChoiceResultType.RECOMMENDATION.value,
            result_recommendation=r3,
        )
        c2.save()

        c3 = Choice(
            question=q2,
            text="Action",
            result_type=ChoiceResultType.RECOMMENDATION.value,
            result_recommendation=r1,
        )
        c3.save()

        c4 = Choice(
            question=q2,
            text="Romance",
            result_type=ChoiceResultType.RECOMMENDATION.value,
            result_recommendation=r2,
        )
        c4.save()