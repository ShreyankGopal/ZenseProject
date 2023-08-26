"""
URL configuration for Study project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views as user_views
from teachers import views as teacher_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'users'
urlpatterns = [
    
    path('Register/', user_views.register, name='register'),
    path('TeacherRegister/', teacher_views.register, name='TeacherRegister'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('teacherlogin/', auth_views.LoginView.as_view(template_name='teachers/login.html'), name='teacherlogin'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('teacherlogout/', auth_views.LogoutView.as_view(template_name='teachers/logout.html'), name='teacherlogout'),

    path("", include("studyapp.urls")),
    path('admin/', admin.site.urls),
    path('profile/', user_views.profile, name='profile'),
    path('quizlist/',user_views.quizlistview,name='quizlist'),
    path('Create_Question/', teacher_views.create_question, name='Create_Question'),
    
    #path('questions/<int:pk>',user_views.questions,name='questions'),
    #path('save_answer/', user_views.save_answer, name='save_answer'),
    path('results/<int:quiz_id>',user_views.results,name='results'),
    path('results/',user_views.quizresults,name='quizresults'),
    path('ThankYou',user_views.thankyou,name='thankyou'),
    path('quizzes/<int:quiz_id>/question/<int:question_id>',user_views.quizquestions,name='quizquestions'),
    path('quizzes/<int:quiz_id>',user_views.access_quiz_questions,name='quizdetail'),
    path('credits/',user_views.credits,name='credits'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)