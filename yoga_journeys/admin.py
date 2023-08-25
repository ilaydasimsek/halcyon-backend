from django.contrib import admin

from yoga_journeys.models import YogaJourney


class YogaPracticeInline(admin.TabularInline):
    model = YogaJourney.completed_yoga_practices.through


@admin.register(YogaJourney)
class YogaJourneyAdmin(admin.ModelAdmin):
    list_display = ["user", "get_completed_practices_count"]
    search_fields = ["user"]
    inlines = [YogaPracticeInline]

    @admin.display(description="# of completed practices")
    def get_completed_practices_count(self, obj: YogaJourney):
        return obj.completed_yoga_practices.count()
