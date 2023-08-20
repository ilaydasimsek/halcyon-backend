from django.db import models


class YogaJourney(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    completed_yoga_practices = models.ManyToManyField(
        "yoga_practices.YogaPractice", through="yoga_journeys.JourneyCompletedYogaPractice", blank=True
    )

    def on_yoga_practice_completed(self, yoga_practice_id):
        JourneyCompletedYogaPractice.objects.create(
            yoga_journey=self,
            yoga_practice_id=yoga_practice_id,
        )


class JourneyCompletedYogaPractice(models.Model):
    class Meta:
        ordering = ["-created_at"]

    yoga_practice = models.ForeignKey("yoga_practices.YogaPractice", on_delete=models.CASCADE)
    yoga_journey = models.ForeignKey(YogaJourney, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
