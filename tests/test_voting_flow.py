from my_prj.test_utils import *


@pytest.mark.django_db
def test_voting_flow():
    user = UserFactory()
    client = APIClient()

    # create poll
    question = QuestionFactory()
    choice = question.choice_set.all().first()

    # login
    resp = client.post(reverse('api.auth.login-list'), data={
        'username': user.username,
        'password': user.initial_password
    })
    assert_that(resp, is_api_response(http_status_code=201, data=anything()))

    # vote
    resp = client.put(
        reverse('api.questions.votes-detail', kwargs={'question_id': question.pk, 'pk': choice.pk}),
        data={})
    assert_that(resp, is_api_response(data=all_of(
        has_keys('id', 'choice_text', 'votes'),
        has_entry('votes', equal_to(1)))))
