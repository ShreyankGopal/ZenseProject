from typing import Any
from django.db import models
import uuid
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='https://campussafetyconference.com/wp-content/uploads/2020/08/iStock-476085198.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
difficulty_choices=(('easy','easy'),('hard','hard'),('medium','medium'))
class Quiz(models.Model):
    name=models.CharField(max_length=200)
    topic=models.CharField(max_length=100)
    difficulty=models.CharField(max_length=100,choices=difficulty_choices)

class Questions(models.Model):
    text=models.CharField(max_length=200)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.text)
class Answers(models.Model):
    text=models.CharField(max_length=200)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    def __str__(self):
        return f"Question:{self.question.text},answer:{self.text},correct:{self.correct}"
    




