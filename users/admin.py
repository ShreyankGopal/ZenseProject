from django.contrib import admin
from .models import Profile,Questions,Answers,Quiz
admin.site.register(Profile)
admin.site.register(Quiz)
class AnswerInline(admin.TabularInline):
    model=Answers
class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]
admin.site.register(Questions,QuestionAdmin)
admin.site.register(Answers)
# Register your models here.