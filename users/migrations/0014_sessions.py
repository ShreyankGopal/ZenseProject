# Generated by Django 4.2.1 on 2023-08-24 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_quiz_attempted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sess', models.IntegerField(default=0)),
            ],
        ),
    ]
