from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class Chakra(models.TextChoices):
    MULADHARA = "Muladhara"
    SVADHISHTHANA = "Svadhishthana"
    MANIPURA = "Manipura"
    ANAHATA = "Anahata"
    VISHUDDHA = "Vishuddha"
    AJNA = "Ajna"
    SAHASRARA = "Sahasrara"


class YogaStyle(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Yoga Style ({self.name})"


class YogaCategory(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Yoga Category ({self.name})"


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
    muscle_groups = models.ManyToManyField(MuscleGroup, blank=True)
    chakras = ArrayField(
        models.CharField(choices=Chakra.choices, max_length=64), blank=False, null=True, default=list, size=7
    )
    styles = models.ManyToManyField(YogaStyle, blank=True)
    categories = models.ManyToManyField(YogaCategory, blank=True)

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


class YogaChallenge(models.Model):
    title = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(blank=False, null=False)
    benefits_description = models.TextField(blank=False, null=False)
    cover_image_url = models.URLField(null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    practices = models.ManyToManyField(YogaPractice, through="YogaChallengePractice")

    def __str__(self):
        return f"Yoga Challenge: {self.title}"


class YogaChallengePractice(models.Model):
    class Meta:
        unique_together = ["yoga_challenge", "order"]
        ordering = ["order", "yoga_challenge__title"]

    yoga_practice = models.ForeignKey(YogaPractice, on_delete=models.CASCADE)
    yoga_challenge = models.ForeignKey(YogaChallenge, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f"Challenge: {self.yoga_challenge.title} - (#{self.order}) Practice: {self.yoga_practice.title}"
