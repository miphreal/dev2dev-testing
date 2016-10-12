from hypothesis import given, strategies as st
from pytest import fixture, mark


@fixture
def stuff():
    return "kittens"


@given(a=st.none())
def test_stuff(a, stuff):
    assert a is None
    assert stuff == "kittens"


@mark.slow
def test_slow_logic():
    pass
