# Generated by Django 5.0.6 on 2024-05-31 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_prediction_questionnaire"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prediction",
            name="questionnaire",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="predictions_q",
                to="users.questionnaire",
            ),
        ),
    ]
