from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    preferredSubjects = models.ManyToManyField('Subject', related_name='preferred_by')
    dislikedSubjects = models.ManyToManyField('Subject', related_name='disliked_by')
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    questionnaireID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    highSchoolGPA = models.FloatField()
    choiceFactors = models.CharField(max_length=255)
    biggestDifficulty = models.CharField(max_length=255)

    def submit(self):
        pass

class Recommendation(models.Model):
    recommendationID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recommendedBranches = models.CharField(max_length=255)

    def generateRecommendations(self):
        pass

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
