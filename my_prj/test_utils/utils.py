from datetime import datetime, timedelta
from functools import partial
import json
from uuid import uuid4

from django.core import mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import SimpleCookie
from django.test import TestCase, RequestFactory
from django.utils import timezone
import factory
from factory.django import mute_signals, DjangoModelFactory
from factory.faker import Faker as FakerData
from factory.fuzzy import *
from faker import Faker
from faker.providers import BaseProvider
from freezegun import freeze_time
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hypothesis import given, strategies as st
import pytest
from pytz import UTC
from rest_framework.test import APITestCase, APIClient
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
FakerData.add_provider(ExtraProvider)


def has_keys(*keys_matchers):
    return has_entries({km: anything() for km in keys_matchers})


def is_string():
    return instance_of(str)


def is_api_response(http_status_code=200, data=None):
    return all_of(
        has_property('content', ApiResponseMatcher(data=data)),
        has_property('status_code', equal_to(http_status_code)),
    )


class ApiResponseMatcher(BaseMatcher):

    def __init__(self, data=anything()):
        self._matcher = wrap_matcher(data)
        self._response = None

    def _matches(self, response):
        return self._matcher.matches(response)

    def matches(self, item, mismatch_description=None):
        if not item:
            if mismatch_description:
                mismatch_description.append_text('api response was empty')
            return False

        try:
            if isinstance(item, bytes):
                item = item.decode('utf-8')
            self._response = json.loads(item) if item is not None else None
        except ValueError as e:
            if mismatch_description:
                mismatch_description.append_text('invalid api response ({})'.format(e))
            return False

        if self._matcher.matches(self._response, mismatch_description):
            return True

        if mismatch_description:
            self.describe_mismatch(item, mismatch_description)
        return False

    def describe_to(self, description):
        description.append_text('api response containing ')\
            .append_description_of(self._matcher)

    def describe_mismatch(self, item, mismatch_description):
        import json
        mismatch_description.append_text('was ')
        try:
            mismatch_description.append_text(json.dumps(self._response, indent=4))
        except ValueError:
            mismatch_description.append_text(item)

        mismatch_description.append_text(' where ')
        self._matcher.describe_mismatch(self._response, mismatch_description)
