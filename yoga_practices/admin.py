from django import forms
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from yoga_practices.models import YogaPose, MuscleGroup, YogaPractice, Chakra, YogaStyle, YogaCategory, YogaChallenge


class YogaPoseForm(forms.ModelForm):
    chakras = forms.MultipleChoiceField(choices=Chakra.choices, required=False)


@admin.register(YogaPose)
class YogaPoseAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["name", "sanskrit_name", "difficulty", "get_muscle_groups"]
    search_fields = ["name"]
    form = YogaPoseForm

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


class YogaPracticeInline(admin.TabularInline):
    model = YogaChallenge.practices.through


@admin.register(YogaChallenge)
class YogaChallengeAdmin(admin.ModelAdmin):
    list_display = ["title", "get_practices_count", "created_by"]
    ordering = ["-created_at"]
    search_fields = ["title"]
    inlines = [YogaPracticeInline]

    @admin.display(description="# of practices")
    def get_practices_count(self, obj: YogaChallenge):
        return obj.practices.count()


@admin.register(YogaStyle)
class YogaStyleAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(YogaCategory)
class YogaCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
