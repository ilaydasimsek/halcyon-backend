from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MuscleGroup(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        return f"Muscle Group ({self.name})"


class YogaPose(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)
    sanskrit_name = models.CharField(blank=False, null=False, max_length=255, help_text="Name in sanskrit language")
    description = models.TextField(blank=False, null=False)

    difficulty = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    muscle_groups = models.ManyToManyField(MuscleGroup, null=True, blank=True)

    audio_url = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Yoga Pose ({self.name})"


class YogaPractice(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=False, null=False)
    benefits_description = models.TextField(blank=False, null=False)
    cover_image_url = models.URLField(null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    yoga_poses = models.ManyToManyField(YogaPose, through="YogaPracticePose")

    def __str__(self):
        return f"Yoga Practice ({self.title})"


class YogaPracticePose(models.Model):
    class Meta:
        unique_together = ["yoga_practice", "order"]
        ordering = ["order", "yoga_practice__title"]

    yoga_practice = models.ForeignKey(YogaPractice, on_delete=models.CASCADE)
    yoga_pose = models.ForeignKey(YogaPose, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f"Practice: {self.yoga_practice.title} - (#{self.order}) Pose: {self.yoga_pose.name}"
