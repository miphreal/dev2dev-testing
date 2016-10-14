from datetime import datetime, timedelta
from functools import partial
import pytest
from uuid import uuid4

from django.core import mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import SimpleCookie
from django.test import TestCase, RequestFactory
import factory
from factory.django import mute_signals, DjangoModelFactory
from factory.faker import *
from factory.fuzzy import *
from faker import Faker
from faker.providers import BaseProvider
from freezegun import freeze_time
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from unittest import mock
from unittest.mock import patch, Mock, MagicMock


fake = Faker()
UserModel = get_user_model()


class ExtraProvider(BaseProvider):
    def uuid(self):
        return uuid4()

    def username(self):
        return fake.bothify('username???##')


fake.add_provider(ExtraProvider)


def has_keys(*keys_matchers):
    return has_entries({km: anything() for km in keys_matchers})


def is_string():
    return instance_of(str)
