from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    high_school_gpa = models.FloatField()
    region = models.CharField(max_length=255)
    preferred_living = models.CharField(max_length=255, default="")
    choice_factors = models.CharField(max_length=255, default="")
    biggest_difficulty = models.CharField(max_length=255, default="")
    preferred_subjects = models.CharField(max_length=255, default="")
    disliked_subjects = models.CharField(max_length=255, default="")
    university_type = models.CharField(max_length=50, default="")
    preferred_study_duration = models.IntegerField(default="4")

class Prediction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    recommended_branches = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class University(models.Model):
    universityID = models.AutoField(primary_key=True)
    universityName = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    specializations = models.ManyToManyField('Specification')

    def addSpecialization(self, spec):
        self.specializations.add(spec)

    def removeSpecialization(self, spec):
        self.specializations.remove(spec)

class Specification(models.Model):
    specificationID = models.AutoField(primary_key=True)
    specificationName = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()

    def __str__(self):
        return self.specificationName
