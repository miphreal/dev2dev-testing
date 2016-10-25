from my_prj.profile.models import User
from my_prj.test_utils import *


class UserManagerTestCase(TestCase):
    def test_create_superuser(self):
        email = fake.email()
        admin_user = User.objects.create_superuser(
            username=fake.username(),
            email=email,
            password=fake.password(10)
        )

        assert_that(admin_user, has_properties(
            email=equal_to(email),
            is_staff=equal_to(True),
            is_active=equal_to(True),
            is_superuser=equal_to(True)))

    def test_create_user(self):
        email = fake.email()
        user = User.objects.create_user(
            username=fake.username(),
            email=email,
            password=fake.password(10)
        )

        assert_that(user, has_properties(
            email=equal_to(email),
            is_staff=equal_to(False),
            is_active=equal_to(True),
            is_superuser=equal_to(False)))
