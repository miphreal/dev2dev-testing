from my_prj.test_utils import *


@pytest.mark.slowtest
def test_slow_logic():
    import time
    import os

    time.sleep(int(os.getenv('NET_LATENCY', 1)))


@mock.patch('django.utils.timezone.now')
def test_world_creation_date(dt_now_mock):
    dt_now_mock.side_effect = lambda: datetime.datetime(1990, 11, 29, tzinfo=UTC)

    assert timezone.now() == datetime.datetime(1990, 11, 29, tzinfo=UTC)


def test_world_creation_date2():
    with freeze_time(datetime.datetime(1990, 11, 29)):
        assert timezone.now() == datetime.datetime(1990, 11, 29, tzinfo=UTC)


@pytest.fixture
def response():
    return {
        'id': 48,
        'name': 'r2d2',
        'functionality': {
            'speed': 'slow',
            'AI': True,
            'languages': [
                {'id': 'en'},
                {'id': 'ru'},
            ]
        }
    }


def test_data_structure(response):

    assert_that(response, has_entries({
        'id': greater_than(0),
        'name': instance_of(str),
        'functionality': has_entries({
            'speed': any_of('slow', 'sloow', 'slooow'),
            'AI': True,
            'languages': all_of(
                has_length(2),
                contains_inanyorder(
                    has_entry('id', 'en'),
                    has_entry('id', 'ru')))})}))
