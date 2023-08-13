from django.contrib import admin

from yoga_practices.models import YogaPose, MuscleGroup, YogaPractice


@admin.register(YogaPose)
class YogaPoseAdmin(admin.ModelAdmin):
    list_display = ["name", "sanskrit_name", "difficulty", "get_muscle_groups"]
    search_fields = ["name"]

    @admin.display(description="Muscle groups")
    def get_muscle_groups(self, obj: YogaPose):
        return ", ".join(obj.muscle_groups.values_list("name", flat=True))


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class YogaPracticePoseInline(admin.TabularInline):
    model = YogaPractice.yoga_poses.through


@admin.register(YogaPractice)
class YogaPracticeAdmin(admin.ModelAdmin):
    list_display = ["title", "get_poses_count", "created_by"]
    ordering = ["-created_at"]
    search_fields = ["title"]
    inlines = [YogaPracticePoseInline]

    @admin.display(description="# of poses")
    def get_poses_count(self, obj: YogaPractice):
        return obj.yoga_poses.count()
