# Generated by Django 5.0.6 on 2024-05-31 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_rename_highschoolgpa_questionnaire_high_school_gpa_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="prediction",
            old_name="recommendationID",
            new_name="id",
        ),
        migrations.RenameField(
            model_name="questionnaire",
            old_name="questionnaireID",
            new_name="id",
        ),
    ]
