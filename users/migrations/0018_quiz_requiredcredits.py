# Generated by Django 4.2.1 on 2023-08-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_quiz_timelimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='RequiredCredits',
            field=models.IntegerField(default=0),
        ),
    ]
