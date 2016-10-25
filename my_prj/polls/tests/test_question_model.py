from my_prj.test_utils import *


class QuestionMethodTests(TestCase):

    def test_question_was_created_recently(self):
        with freeze_time(timezone.now() - timedelta(days=30)):
            q = QuestionFactory()

        assert not q.was_created_recently()


@pytest.mark.django_db
def test_active_question():
    pub_date = timezone.now() + timedelta(days=10)

    q = QuestionFactory(pub_date=pub_date)
    assert not q.is_active_question()

    with freeze_time(pub_date):
        assert q.is_active_question()
