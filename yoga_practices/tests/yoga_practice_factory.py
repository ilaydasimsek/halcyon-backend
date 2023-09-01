from yoga_practices.models import YogaPractice, YogaStyle, YogaChallenge, YogaChallengePractice


def yoga_practice_factory(**kwargs):
    kwargs.setdefault("title", "Fake Yoga Practice Title")
    kwargs.setdefault("description", "Fake Yoga Practice Description")
    kwargs.setdefault("benefits_description", "Fake Yoga Practice Benefits Description")
    if kwargs.get("style") is None and kwargs.get("style_id") is None:
        kwargs["style"] = yoga_style_factory()

    return YogaPractice.objects.create(**kwargs)


def yoga_style_factory(**kwargs):
    kwargs.setdefault("name", "Fake Yoga Style")

    return YogaStyle.objects.create(**kwargs)


def yoga_challenge_factory(yoga_practice_count=0, **kwargs):
    kwargs.setdefault("title", "Fake Yoga Practice Title")
    kwargs.setdefault("description", "Fake Yoga Practice Description")
    kwargs.setdefault("benefits_description", "Fake Yoga Practice Benefits Description")
    yoga_challenge = YogaChallenge.objects.create(**kwargs)

    for i in range(yoga_practice_count):
        YogaChallengePractice.objects.create(
            order=i, yoga_practice=yoga_practice_factory(), yoga_challenge=yoga_challenge
        )
    return yoga_challenge
