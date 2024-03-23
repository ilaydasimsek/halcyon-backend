import logging

from django.conf import settings
from django.db import IntegrityError, transaction

from articles.models import Article, ArticleContentItems, ArticleImageContentItem, ArticleTextContentItem
from dev.test_data.data.articles_data import ARTICLES
from dev.test_data.data.yoga_challenges_data import YOGA_CHALLENGES
from dev.test_data.data.yoga_lesson_data import YOGA_LESSONS
from dev.test_data.data.yoga_practices_data import (
    MUSCLE_GROUP_NAMES,
    YOGA_CATEGORY_NAMES,
    YOGA_STYLE_NAMES,
    YOGA_POSES,
    YOGA_PRACTICES,
)
from yoga_lessons.models import YogaLesson, YogaLessonArticleStep, YogaLessonPracticeStep
from yoga_practices.models import (
    YogaPractice,
    MuscleGroup,
    YogaCategory,
    YogaStyle,
    YogaPose,
    YogaChallenge,
    YogaChallengePractice,
    YogaPracticePose,
)

logger = logging.getLogger(__name__)


def populate_muscle_groups():
    for name in MUSCLE_GROUP_NAMES:
        try:
            MuscleGroup.objects.create(name=name)
            logger.info(f"Populated Muscle Group ({name})")
        except IntegrityError:
            pass


def populate_yoga_categories():
    objects = []
    for name in YOGA_CATEGORY_NAMES:
        if not YogaCategory.objects.filter(name=name).exists():
            logger.info(f"Populating Yoga Category ({name})")
            objects.append(YogaCategory(name=name, description=f"{name} - description"))
    YogaCategory.objects.bulk_create(objects)


def populate_yoga_style():
    objects = []
    for name in YOGA_STYLE_NAMES:
        if not YogaStyle.objects.filter(name=name).exists():
            logger.info(f"Populating Yoga Style ({name})")
            objects.append(YogaStyle(name=name, description=f"{name} - description"))
    YogaStyle.objects.bulk_create(objects)


def populate_yoga_poses():
    from yoga_practices.models import YogaPose, MuscleGroup

    for pose in YOGA_POSES:
        if not YogaPose.objects.filter(name=pose["name"]).exists():
            muscle_groups = pose.pop("muscle_groups")
            obj = YogaPose.objects.create(**pose)
            for muscle_group in muscle_groups:
                obj.muscle_groups.add(MuscleGroup.objects.get(name=muscle_group))

            logger.info(f"Populated Yoga Pose ({pose['name']})")


def populate_yoga_practices():
    for practice in YOGA_PRACTICES:
        title = practice["title"]
        if not YogaPractice.objects.filter(title=title).exists():
            style_name = practice.pop("style")
            poses = practice.pop("poses")
            yoga_practice = YogaPractice.objects.create(
                created_by="Halcyon", style=YogaStyle.objects.get(name=style_name), **practice
            )
            for order, pose in enumerate(poses):
                YogaPracticePose.objects.create(
                    yoga_practice=yoga_practice, yoga_pose=YogaPose.objects.get(name=pose["name"]), order=order
                )
            logger.info(f"Populated Yoga Practice ({title})")


def populate_yoga_challenges():
    for challenge in YOGA_CHALLENGES:
        title = challenge["title"]
        if not YogaChallenge.objects.filter(title=title).exists():
            practices = challenge.pop("practices")
            yoga_challenge = YogaChallenge.objects.create(created_by="Halcyon", **challenge)
            # Populate practices
            for order, practice in enumerate(practices):
                YogaChallengePractice.objects.create(
                    yoga_challenge=yoga_challenge,
                    yoga_practice=YogaPractice.objects.get(title=practice["title"]),
                    order=order,
                )
            logger.info(f"Populated Yoga Challenge ({title})")


def create_content_item(item):
    type = item["type"]
    if type == "image":
        return ArticleImageContentItem(**item)
    elif type == "text":
        return ArticleTextContentItem(**item)
    raise ValueError(f"Unknown item type {type}")


def populate_articles():
    for article in ARTICLES:
        title = article["title"]
        if Article.objects.filter(title=title).exists():
            continue
        items = []
        for item in article["content_items"]:
            items.append(create_content_item(item))
        Article.objects.create(
            title=title,
            content_items=ArticleContentItems(items=items),
        )
        logger.info(f"Populated Article ({title})")


def populate_yoga_lessons():
    for i, lesson in enumerate(YOGA_LESSONS):
        title = lesson["title"]
        if YogaLesson.objects.filter(title=title).exists():
            continue
        yoga_lesson = YogaLesson.objects.create(**lesson)
        for order in range(i + 1):
            if (i + order) % 3 == 0:
                YogaLessonArticleStep.objects.create(
                    yoga_lesson=yoga_lesson, order=order, article=Article.objects.all()[i % 4]
                )
            else:
                YogaLessonPracticeStep.objects.create(
                    yoga_lesson=yoga_lesson, order=order, yoga_practice=YogaPractice.objects.all()[i % 4]
                )

        logger.info(f"Populated Yoga Lesson ({title})")


def clean_data():
    Models = [MuscleGroup, YogaCategory, YogaPractice, YogaStyle, YogaPose, YogaChallenge, Article, YogaLesson]

    for Model in Models:
        Model.objects.all().delete()

    logger.info("Existing data cleaned.")


def populate(clean_existing_data=False):
    if not settings.IS_DEV:
        raise Exception("This can be run only in development mode.")

    with transaction.atomic():
        if clean_existing_data:
            clean_data()

        populate_muscle_groups()
        populate_yoga_categories()
        populate_yoga_style()
        populate_yoga_poses()
        populate_yoga_practices()
        populate_yoga_challenges()
        populate_articles()
        populate_yoga_lessons()
