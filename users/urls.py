from django.urls import include, path
from users import views as uviews
urlpatterns=[
    #path('<int:pk>',uviews.quizdetailview,name='quizdetails'),
    path('<int:pk>',uviews.quizquestions,name='quizquestions')
]