from yoga_practices.models import YogaPractice, YogaStyle


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
