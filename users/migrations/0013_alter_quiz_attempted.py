# Generated by Django 4.2.1 on 2023-08-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_quiz_attempted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='Attempted',
            field=models.IntegerField(default=0),
        ),
    ]
