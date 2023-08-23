from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm,QuizForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Quiz,Questions,Answers,UserAnswer,Results
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
@login_required
def profile(request):
    try:
        profile_instance = request.user.profile
    except Profile.DoesNotExist:
        # If the Profile instance doesn't exist, create a new one
        profile_instance = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_instance)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)




def quizlistview(request):
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request, 'users/QuizList.html', context)
    #return HttpResponse('<h1>hi</h1>')







@login_required
def quizdetailview(request,pk):
    quiz_instance=Quiz.objects.get(pk=pk)
    context={'quizdetail':quiz_instance}
    return render(request,'users/quizdetail.html',context)
def quizquestions(request, quiz_id, question_id):
    

    # Check if the user accessed the URL through the appropriate button
    #if not request.session.get('quiz_questions_accessed'):
        #return HttpResponseForbidden("Access denied")
    Hi=request.session.get('quiz_questions_accessed')
    quiz_instance = get_object_or_404(Quiz, pk=quiz_id)
    
    question_instance = get_object_or_404(Questions, pk=question_id, quiz=quiz_instance)
    

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=question_instance)
        if form.is_valid():
            selected_answer_id = request.POST.get("selected_answer")
            selected_answer = Answers.objects.get(id=selected_answer_id)
            question_answered = selected_answer.question
            user_answer = form.save(commit=False)
            user_answer, created = UserAnswer.objects.get_or_create(
                user=request.user,
                question=question_answered
            )
            user_answer.quiz = quiz_instance
            user_answer.answer = selected_answer
            user_answer.save()

            next_question_id = question_id + 1
            if next_question_id <= quiz_instance.number_of_questions:
                return redirect('quizquestions',quiz_id=quiz_id,question_id=next_question_id)
            else:
                # Quiz is complete, redirect to the result page
                return redirect('results')
    else:
        form = QuizForm(instance=question_instance)
    
    context = {'form': form, 'quiz': quiz_instance, 'question': question_instance,'Hi':Hi}
    
    return render(request, 'users/quiz.html', context)

@login_required
def results(request):
    BASE_URL="http://127.0.0.1:8000/"
    users=request.user
    quizs=Quiz.objects.all()
    results=[]
    reviews=[]
    for quiz in quizs:
            review=[]
            res,created=Results.objects.get_or_create(user=request.user,quiz=quiz)

            for question in quiz.get_questions():
                if UserAnswer.objects.filter(user=request.user,quiz=quiz,question=question).exists():
                    userans=UserAnswer.objects.get(user=request.user,quiz=quiz,question=question)
                
                    if(str(question.correct)==str(userans.answer.text)):
                        review.append({question.text:[userans.answer.text,question.correct,'✅']})
                        res.correct=res.correct+1
                        res.totalmarks=res.totalmarks+1
                    else:
                        review.append({question.text:[userans.answer.text,question.correct,'❌']})
                        res.wrong=res.wrong+1
            
            results.append([res,review])
    context={'results':results,
            'review':reviews,
            'BASE_URL':BASE_URL}
    return render(request,'users/results.html',context)
'''class YourView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        try:
            if self.request.META.get('HTTP_REFERER') == BASE_URL + reverse('users:results'):
                return redirect('app_name:home_page_name')
            else:
                return super().get(request, *args, **kwargs)
        except Exception:
            return super().get(request, *args, **kwargs)'''
'''@login_required
def thankyou(request):
    return render(request,'users/ThankYouPage.html')'''
@login_required
def quizdetail(request,pk):
    quiz_instance=Quiz.objects.get(pk=pk)
    context={
        'quiz':quiz_instance
    }
    return render(request,'users/quizdetail.html',context)
@login_required

def access_quiz_questions(request, quiz_id, question_id):
    if request.method == 'POST':
        # Set a session variable to indicate the button was clicked
        request.session['quiz_questions_accessed'] = "YES"
        return redirect('quizquestions', quiz_id=quiz_id, question_id=question_id)

    # Reset the session variable if it's not a form submission
    request.session['quiz_questions_accessed'] = "NO"

    return render(request, 'users/quizdetail.html')

              


        

