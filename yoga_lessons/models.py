from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class YogaLesson(models.Model):
    class Meta:
        ordering = ["-priority"]

    title = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=False, null=False)
    cover_image_url = models.URLField(null=True, blank=True)

    priority = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(4)], help_text="Used as an ordering criteria"
    )

    @property
    def steps_count(self):
        return self.steps.count()

    @property
    def duration(self):
        return self.steps.aggregate(models.Sum("duration")).get("duration__sum") or 0


class YogaLessonStep(models.Model):
    class Meta:
        ordering = ["order"]

    yoga_lesson = models.ForeignKey(YogaLesson, on_delete=models.CASCADE, related_name="steps")

    title = models.CharField(blank=False, null=False, max_length=255)
    duration = models.IntegerField(validators=[MinValueValidator(1)], help_text="duration in seconds")
    audio_url = models.URLField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    order = models.PositiveSmallIntegerField(null=False, blank=False, default=0)


class JourneyActiveYogaLesson(models.Model):
    class Meta:
        ordering = ["-created_at"]
        unique_together = ["yoga_lesson", "yoga_journey"]

    yoga_lesson = models.ForeignKey("yoga_lessons.YogaLesson", on_delete=models.CASCADE)
    yoga_journey = models.ForeignKey("yoga_journeys.YogaJourney", on_delete=models.CASCADE)
    completed_lesson_steps = models.ManyToManyField("yoga_lessons.YogaLessonStep")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
