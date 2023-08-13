from django.contrib import admin

from yoga_practices.models import YogaPose, MuscleGroup, YogaPractice


@admin.register(YogaPose)
class YogaPoseAdmin(admin.ModelAdmin):
    list_display = ["name", "sanskrit_name", "difficulty", "get_muscle_group_count"]
    search_fields = ["name"]

    @admin.display(description="# of muscle groups")
    def get_muscle_group_count(self, obj: YogaPose):
        return obj.muscle_groups.count()


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class YogaPracticePoseInline(admin.TabularInline):
    model = YogaPractice.yoga_poses.through


@admin.register(YogaPractice)
class YogaPracticeAdmin(admin.ModelAdmin):
    list_display = ["title", "get_poses", "created_by"]
    ordering = ["-created_at"]
    search_fields = ["title"]
    inlines = [YogaPracticePoseInline]

    @admin.display(description="Poses")
    def get_poses(self, obj: YogaPractice):
        return ", ".join(obj.yoga_poses.values_list("name", flat=True))
