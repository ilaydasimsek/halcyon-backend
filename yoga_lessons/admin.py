from django.contrib import admin

from yoga_lessons.models import YogaLessonStep, YogaLesson, YogaLessonPracticeStep, YogaLessonArticleStep


from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline


class YogaLessonStepInline(StackedPolymorphicInline):
    """
    https://django-polymorphic.readthedocs.io/en/latest/admin.html
    """

    class YogaPracticeStepInline(StackedPolymorphicInline.Child):
        model = YogaLessonPracticeStep

    class ArticleStepInline(StackedPolymorphicInline.Child):
        model = YogaLessonArticleStep

    model = YogaLessonStep
    child_inlines = (
        YogaPracticeStepInline,
        ArticleStepInline,
    )


@admin.register(YogaLesson)
class YogaLessonAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    list_display = ["title", "steps_count", "priority"]
    search_fields = ["title"]
    inlines = [YogaLessonStepInline]
