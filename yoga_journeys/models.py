from django.db import models


class YogaJourney(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    completed_yoga_practices = models.ManyToManyField(
        "yoga_practices.YogaPractice", through="yoga_journeys.JourneyCompletedYogaPractice", blank=True
    )
    active_yoga_challenges = models.ManyToManyField(
        "yoga_practices.YogaChallenge", through="yoga_journeys.JourneyActiveYogaChallenge", blank=True
    )

    def complete_yoga_practice(self, yoga_practice_id):
        JourneyCompletedYogaPractice.objects.create(
            yoga_journey=self,
            yoga_practice_id=yoga_practice_id,
        )

    def start_yoga_challenge(self, yoga_challenge_id):
        JourneyActiveYogaChallenge.objects.create(yoga_journey=self, yoga_challenge_id=yoga_challenge_id)

    def complete_yoga_challenge_practice(self, yoga_challenge_id, yoga_practice_id):
        active_yoga_challenge = JourneyActiveYogaChallenge.objects.get(
            yoga_journey=self, yoga_challenge_id=yoga_challenge_id
        )
        active_yoga_challenge.completed_yoga_practices.add(yoga_practice_id)


class JourneyCompletedYogaPractice(models.Model):
    class Meta:
        ordering = ["-created_at"]

    yoga_practice = models.ForeignKey("yoga_practices.YogaPractice", on_delete=models.CASCADE)
    yoga_journey = models.ForeignKey(YogaJourney, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class JourneyActiveYogaChallenge(models.Model):
    class Meta:
        ordering = ["-activated_at"]
        unique_together = ["yoga_challenge", "yoga_journey"]

    yoga_challenge = models.ForeignKey("yoga_practices.YogaChallenge", on_delete=models.CASCADE)
    yoga_journey = models.ForeignKey(YogaJourney, on_delete=models.CASCADE)
    completed_yoga_practices = models.ManyToManyField("yoga_practices.YogaPractice")
    activated_at = models.DateTimeField(auto_now_add=True, editable=False)
