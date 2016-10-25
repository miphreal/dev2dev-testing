from my_prj.test_utils import *


class QuestionsApiTestCase(APITestCase):

    def test_get_list_of_questions(self):
        question = QuestionFactory(pub_date=timezone.now())

        resp = self.client.get(reverse('api.questions-list'))
        assert_that(
            resp,
            is_api_response(data=all_of(
                only_contains(has_entries({
                    'id': equal_to(question.pk),
                    'question_text': equal_to(question.question_text),
                    'choices': only_contains(
                        has_keys('id', 'choice_text', 'votes')
                    )
                })),
                has_length(1))))
