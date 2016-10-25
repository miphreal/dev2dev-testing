from my_prj.profile.models import User
from my_prj.test_utils import *


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('username')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    is_staff = False
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        user = manager.create_user(*args, **kwargs)
        user.initial_password = kwargs['password']
        return user
