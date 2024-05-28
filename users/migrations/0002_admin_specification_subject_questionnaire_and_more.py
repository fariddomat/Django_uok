# Generated by Django 5.0.6 on 2024-05-28 16:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Admin",
            fields=[
                ("adminID", models.AutoField(primary_key=True, serialize=False)),
                ("adminName", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Specification",
            fields=[
                (
                    "specificationID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("specificationName", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("requirements", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Questionnaire",
            fields=[
                (
                    "questionnaireID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("highSchoolGPA", models.FloatField()),
                ("choiceFactors", models.CharField(max_length=255)),
                ("biggestDifficulty", models.CharField(max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Recommendation",
            fields=[
                (
                    "recommendationID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("recommendedBranches", models.CharField(max_length=255)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="customuser",
            name="dislikedSubjects",
            field=models.ManyToManyField(
                related_name="disliked_by", to="users.subject"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="preferredSubjects",
            field=models.ManyToManyField(
                related_name="preferred_by", to="users.subject"
            ),
        ),
        migrations.CreateModel(
            name="University",
            fields=[
                ("universityID", models.AutoField(primary_key=True, serialize=False)),
                ("universityName", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=50)),
                ("specializations", models.ManyToManyField(to="users.specification")),
            ],
        ),
    ]