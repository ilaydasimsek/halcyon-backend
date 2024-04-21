from django.db import models

from yoga_lessons.models import JourneyActiveYogaLesson
from yoga_practices.models import JourneyCompletedYogaPractice, JourneyActiveYogaChallenge


class YogaJourney(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    completed_yoga_practices = models.ManyToManyField(
        "yoga_practices.YogaPractice", through="yoga_practices.JourneyCompletedYogaPractice", blank=True
    )
    active_yoga_challenges = models.ManyToManyField(
        "yoga_practices.YogaChallenge", through="yoga_practices.JourneyActiveYogaChallenge", blank=True
    )
    active_yoga_lessons = models.ManyToManyField(
        "yoga_lessons.YogaLesson", through="yoga_lessons.JourneyActiveYogaLesson", blank=True
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

    def start_yoga_lesson(self, yoga_lesson_id):
        JourneyActiveYogaLesson.objects.create(yoga_journey=self, yoga_lesson_id=yoga_lesson_id)

    def complete_yoga_lesson_step(self, yoga_lesson_id, yoga_lesson_step_id):
        active_yoga_lesson = JourneyActiveYogaLesson.objects.get(yoga_journey=self, yoga_lesson_id=yoga_lesson_id)
        active_yoga_lesson.completed_lesson_steps.add(yoga_lesson_step_id)

    def restart_yoga_lesson(self, yoga_lesson_id):
        active_yoga_lesson = JourneyActiveYogaLesson.objects.get(yoga_journey=self, yoga_lesson_id=yoga_lesson_id)
        active_yoga_lesson.completed_lesson_steps.all().delete()
