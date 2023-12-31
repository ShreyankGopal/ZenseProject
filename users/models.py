from typing import Any
from django.db import models
import uuid
from django.contrib.auth.models import User
import random



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='https://campussafetyconference.com/wp-content/uploads/2020/08/iStock-476085198.jpg', upload_to='profile_pics')
    credits=models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} Profile'
difficulty_choices=(('easy','easy'),('hard','hard'),('medium','medium'))
class Quiz(models.Model):
    
    topic=models.CharField(max_length=100)
    number_of_questions=models.IntegerField()
    difficulty=models.CharField(max_length=100,choices=difficulty_choices)
    RequiredCredits=models.IntegerField(default=0)
    Attempted=models.IntegerField(default=0)
    def get_questions(self):
        questions=list(self.questions_set.all())
        random.shuffle(questions)
        return self.questions_set.all()
    def __str__(self):
        return self.topic


class Questions(models.Model):
    text=models.CharField(max_length=200)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    correct=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.text)
    def get_answers(self):
        return self.answers_set.all()
class Answers(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    def __str__(self):
        return f"Question: {self.question.text}, Answer: {self.text}"
class UserAnswer(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE,null=True,blank=True)   
    
class Results(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    correct=models.IntegerField(default=0)
    wrong=models.IntegerField(default=0)
    totalmarks=models.IntegerField(default=0)
class Sessions(models.Model):
    sess=models.IntegerField(default=0)  
    


