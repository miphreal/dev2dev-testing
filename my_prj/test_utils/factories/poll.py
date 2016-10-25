from my_prj.polls.models import Question, Choice
from my_prj.test_utils import *


class ChoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Choice

    choice_text = factory.Faker('text')
    votes = 0


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    question_text = factory.Faker('text')
    pub_date = FuzzyAttribute(lambda: timezone.now() + timedelta(days=7))

    @factory.post_generation
    def choices(self, create, extracted, **kwargs):
        if create and not extracted:
            ChoiceFactory.create_batch(5, question=self)
