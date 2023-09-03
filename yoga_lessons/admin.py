from django.contrib import admin

from yoga_lessons.models import YogaLessonStep, YogaLesson


class YogaLessonStepInline(admin.TabularInline):
    model = YogaLessonStep


@admin.register(YogaLesson)
class YogaLessonAdmin(admin.ModelAdmin):
    list_display = ["title", "steps_count", "get_duration"]
    search_fields = ["title"]
    inlines = [YogaLessonStepInline]

    @admin.display(description="Duration (minutes)")
    def get_duration(self, obj: YogaLesson):
        return obj.duration // 60
