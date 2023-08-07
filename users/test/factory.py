from users.models import User


def user_factory(*args, **kwargs):
    kwargs.setdefault("email", "fakee@fake.com")
    kwargs.setdefault("password", "FakePassword123")
    return User.objects.create_user(**kwargs)
