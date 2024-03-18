import logging

from django.core.management import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from articles.models import Article
from yoga_practices.models import Chakra, YogaPractice

logger = logging.getLogger(__name__)

MUSCLE_GROUP_NAMES = ["biceps", "neck", "calves"]
YOGA_CATEGORY_NAMES = ["beginner", "intermediate", "advanced"]
YOGA_STYLE_NAMES = ["yin", "hatha", "vinyasa"]
COMPLEX_YOGA_POSE_NAME = "Complex Yoga Pose"
BASIC_YOGA_POSE_NAME = "Basic Yoga Pose"


def populate_muscle_groups():
    from yoga_practices.models import MuscleGroup

    for name in MUSCLE_GROUP_NAMES:
        try:
            MuscleGroup.objects.create(name=name)
            logger.info(f"Populated Muscle Group ({name})")
        except IntegrityError:
            pass


def populate_yoga_categories():
    from yoga_practices.models import YogaCategory

    objects = []
    for name in YOGA_CATEGORY_NAMES:
        if not YogaCategory.objects.filter(name=name).exists():
            logger.info(f"Populating Yoga Category ({name})")
            objects.append(YogaCategory(name=name, description=f"{name} - description"))
    YogaCategory.objects.bulk_create(objects)


def populate_yoga_style():
    from yoga_practices.models import YogaStyle

    objects = []
    for name in YOGA_STYLE_NAMES:
        if not YogaStyle.objects.filter(name=name).exists():
            logger.info(f"Populating Yoga Style ({name})")
            objects.append(YogaStyle(name=name, description=f"{name} - description"))
    YogaStyle.objects.bulk_create(objects)


def populate_yoga_poses():
    from yoga_practices.models import YogaPose, MuscleGroup, YogaCategory

    if not YogaPose.objects.filter(name=COMPLEX_YOGA_POSE_NAME).exists():
        obj = YogaPose.objects.create(
            name=COMPLEX_YOGA_POSE_NAME,
            sanskrit_name=f"{COMPLEX_YOGA_POSE_NAME} in sanskrit",
            description=f"{COMPLEX_YOGA_POSE_NAME} description",
            difficulty=50,
            chakras=[Chakra.MANIPURA, Chakra.SAHASRARA, Chakra.AJNA],
            audio_url="https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
            image_url="https://picsum.photos/200",
            duration=20,
        )
        for muscle_group in MuscleGroup.objects.filter(name__in=MUSCLE_GROUP_NAMES):
            obj.muscle_groups.add(muscle_group)
        for yoga_category in YogaCategory.objects.filter(name__in=YOGA_CATEGORY_NAMES):
            obj.categories.add(yoga_category)
        logger.info(f"Populated Yoga Pose ({COMPLEX_YOGA_POSE_NAME})")

    if not YogaPose.objects.filter(name=BASIC_YOGA_POSE_NAME).exists():
        YogaPose.objects.create(
            name=BASIC_YOGA_POSE_NAME,
            sanskrit_name=f"{BASIC_YOGA_POSE_NAME} in sanskrit",
            description=f"{BASIC_YOGA_POSE_NAME} description",
            difficulty=10,
            duration=20,
        )
        logger.info(f"Populated Yoga Pose ({BASIC_YOGA_POSE_NAME})")


def populate_yoga_practices():
    from yoga_practices.models import YogaPractice, YogaStyle, YogaPose, YogaPracticePose

    for i in range(1, 6):
        title = f"Yoga Practice #{i}"
        if not YogaPractice.objects.filter(title=title).exists():
            yoga_practice = YogaPractice.objects.create(
                title=title,
                description=f"{title} description",
                benefits_description=f"{title} benefits",
                cover_image_url="https://picsum.photos/400/200",
                created_by="Halcyon",
                style=YogaStyle.objects.get(name=YOGA_STYLE_NAMES[i % len(YOGA_STYLE_NAMES)]),
            )
            if i == 4:
                YogaPracticePose.objects.create(yoga_practice=yoga_practice, yoga_pose=YogaPose.objects.all()[0])
            elif i == 5:
                YogaPracticePose.objects.create(yoga_practice=yoga_practice, yoga_pose=YogaPose.objects.all()[1])
            else:
                YogaPracticePose.objects.create(yoga_practice=yoga_practice, yoga_pose=YogaPose.objects.all()[0])
                YogaPracticePose.objects.create(
                    yoga_practice=yoga_practice, yoga_pose=YogaPose.objects.all()[1], order=1
                )
            logger.info(f"Populated Yoga Practice ({title})")


def populate_yoga_challenges():
    from yoga_practices.models import YogaChallenge, YogaChallengePractice, YogaPractice

    for i in range(1, 6):
        title = f"Yoga Challenge #{i}"
        if not YogaChallenge.objects.filter(title=title).exists():
            yoga_challenge = YogaChallenge.objects.create(
                title=title,
                description=f"{title} description",
                benefits_description=f"{title} benefits",
                cover_image_url="https://picsum.photos/400/200",
                created_by="Halcyon",
            )
            # Populate practices
            order = 0
            for yoga_practice in YogaPractice.objects.all()[:i]:
                YogaChallengePractice.objects.create(
                    yoga_challenge=yoga_challenge, yoga_practice=yoga_practice, order=order
                )
                order += 1
            logger.info(f"Populated Yoga Challenge ({title})")


def populate_articles():
    from articles.models import ArticleContentItems, ArticleImageContentItem, ArticleTextContentItem

    for i in range(1, 6):
        title = f"Article #{i}"
        if Article.objects.filter(title=title).exists():
            continue
        Article.objects.create(
            title=title,
            content_items=ArticleContentItems(
                items=[
                    ArticleImageContentItem(type="image", image_url="https://picsum.photos/400/200"),
                    ArticleTextContentItem(type="text", content="Some Example Content"),
                    ArticleTextContentItem(type="text", content="Some More Example Content"),
                ]
            ),
        )


def populate_yoga_lessons():
    from yoga_lessons.models import YogaLesson, YogaLessonArticleStep, YogaLessonPracticeStep

    for i in range(1, 6):
        title = f"Yoga lesson #{i}"
        if YogaLesson.objects.filter(title=title).exists():
            continue
        yoga_lesson = YogaLesson.objects.create(
            title=title,
            description=f"{title} description",
            cover_image_url="https://picsum.photos/400/200",
            priority=i % 3,
        )
        for order in range(i + 1):
            if (i + order) % 3 == 0:
                YogaLessonArticleStep.objects.create(
                    yoga_lesson=yoga_lesson, order=order, article=Article.objects.all()[i - 1]
                )
            else:
                YogaLessonPracticeStep.objects.create(
                    yoga_lesson=yoga_lesson, order=order, yoga_practice=YogaPractice.objects.all()[i - 1]
                )

        logger.info(f"Populated Yoga Lesson ({title})")


class Command(BaseCommand):
    help = "Populates data for dev environment"

    def handle(self, *args, **options):
        if not settings.IS_DEV:
            raise Exception("This can be run only in development mode.")
        populate_muscle_groups()
        populate_yoga_categories()
        populate_yoga_style()
        populate_yoga_poses()
        populate_yoga_practices()
        populate_yoga_challenges()
        populate_articles()
        populate_yoga_lessons()
