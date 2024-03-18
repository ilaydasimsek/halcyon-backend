from typing import Union

from articles.models import Article
from yoga_lessons.models import YogaLesson, YogaLessonArticleStep, YogaLessonPracticeStep
from yoga_practices.models import YogaPractice


def yoga_lesson_factory(steps: list[Union[Article, YogaPractice]] = None, **kwargs):
    if steps is None:
        steps = []
    kwargs.setdefault("title", "Fake Yoga Lesson")
    kwargs.setdefault("description", "Fake Yoga Lesson Description")
    kwargs.setdefault("priority", 0)
    yoga_lesson = YogaLesson.objects.create(**kwargs)

    for order, step in enumerate(steps):
        if isinstance(step, Article):
            YogaLessonArticleStep.objects.create(yoga_lesson=yoga_lesson, article=step, order=order)
        elif isinstance(step, YogaPractice):
            YogaLessonPracticeStep.objects.create(yoga_lesson=yoga_lesson, yoga_practice=step, order=order)

    return yoga_lesson
