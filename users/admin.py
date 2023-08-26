from django.contrib import admin
from .models import Profile,Questions,Answers,Quiz,UserAnswer,Results,Sessions
admin.site.register(Profile)
admin.site.register(Quiz)
admin.site.register(UserAnswer)
admin.site.register(Results)
class AnswerInline(admin.TabularInline):
    model=Answers
class QuestionAdmin(admin.ModelAdmin):
    inlines=[AnswerInline]
admin.site.register(Questions,QuestionAdmin)
admin.site.register(Answers)
admin.site.register(Sessions)
# Register your models here.
