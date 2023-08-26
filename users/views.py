from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm,QuizForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Quiz,Questions,Answers,UserAnswer,Results,Sessions
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views import View
import os
import random
from .graphs import get_graph

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
    request.session['clicked']=0
    results=Results.objects.filter(user=request.user)
    
    
    try:
        profile_instance = request.user.profile
    except Profile.DoesNotExist:
        # If the Profile instance doesn't exist, create a new one
        profile_instance = Profile.objects.create(user=request.user)
    profile_instance.credits=0
    for res in results:
        
        if (res.totalmarks/res.quiz.number_of_questions)*100 >= 40 and (res.totalmarks/res.quiz.number_of_questions)*100<60:
            profile_instance.credits+=20
        if (res.totalmarks/res.quiz.number_of_questions)*100 >= 60 and (res.totalmarks/res.quiz.number_of_questions)*100<80:
            profile_instance.credits+=40
        if (res.totalmarks/res.quiz.number_of_questions)*100 >= 80 and (res.totalmarks/res.quiz.number_of_questions)*100<100:
            profile_instance.credits+=60
        if (res.totalmarks/res.quiz.number_of_questions)*100==100:
            profile_instance.credits+=100
    profile_instance.save()
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
    get_graph(request.user)
    #graph_path = os.path.join(os.getcwd(), "graph.png")
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile':profile_instance,
        #'graph_path':graph_path
        
    }
    

    return render(request, 'users/profile.html', context)




def quizlistview(request):
    request.session['clicked']=0
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request, 'users/QuizList.html', context)
    
def quizquestions(request, quiz_id, question_id):
    
    
    # Check if the user accessed the URL through the appropriate button
    if not request.session.get('clicked'):
        return redirect('quizdetail',quiz_id=quiz_id)
    
    
    quiz_instance = get_object_or_404(Quiz, pk=quiz_id)
    
    question_instance = get_object_or_404(Questions, pk=question_id, quiz=quiz_instance)
    qlist=[]
    for q in quiz_instance.get_questions():
        qid=q.id
        qlist.append(qid)
    
            
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
            
                
            request.session[f'{quiz_id}']+=1
            while(1):
                randid=random.choice(qlist)
                if(request.session[f'{randid}']==0):
                    break
           
            
            
            
            if  quiz_instance.number_of_questions>=request.session[f'{quiz_id}']:
                request.session[f'{randid}']=1
                next_question_id = randid
                return redirect('quizquestions',quiz_id=quiz_id,question_id=next_question_id)
            else:
                # Quiz is complete, redirect to the result page
                return redirect('results',quiz_id=quiz_id)
            
    else:
        form = QuizForm(instance=question_instance)
    
    context = {'form': form, 'quiz': quiz_instance, 'question': question_instance,}
    
    return render(request, 'users/quiz.html', context)

@login_required
def results(request,quiz_id):
    
    
    users=request.user
    quiz=get_object_or_404(Quiz,pk=quiz_id)
    results=[]
    reviews=[]
    
    review=[]      
    res,created=Results.objects.get_or_create(user=request.user,quiz=quiz)
    res.correct=0
    res.wrong=0
    res.totalmarks=0
    res.save()
    for question in quiz.get_questions():
        
        if UserAnswer.objects.filter(user=request.user,quiz=quiz,question=question).exists():
            if request.session[f'{question.id}']==1:
                userans=UserAnswer.objects.get(user=request.user,quiz=quiz,question=question)
            else:
                continue   
            if(str(question.correct)==str(userans.answer.text)):
                review.append({question.text:[userans.answer.text,question.correct,'✅']})
                res.correct=res.correct+1
                res.totalmarks=res.totalmarks+1
            else:
                review.append({question.text:[userans.answer.text,question.correct,'❌']})
                res.wrong=res.wrong+1
    res.save()
    
    number=quiz.number_of_questions+1      
    results.append([res,review])
    context={'results':results,
            'review':reviews,
            'quiz':quiz,
            'number':number
            }
    request.session['clicked']=0
    return render(request,'users/results.html',context)


@login_required

def access_quiz_questions(request, quiz_id):
    #session,created=Sessions.objects.get_or_create(id=1)
    
    quiz_inst=Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        # Set a session variable to indicate the button was click
        request.session['clicked']=1
        request.session[f'{quiz_id}']=0
        quiz_inst=Quiz.objects.get(id=quiz_id)
        qlist=[]
        for q in quiz_inst.get_questions():
            qid=q.id
            request.session[f'{qid}']=0
            qlist.append(qid)
        randid=random.choice(qlist)
        request.session[f'{randid}']=1
        
        
        return redirect('quizquestions', quiz_id=quiz_id, question_id=randid)

    # Reset the session variable if it's not a form submission
    request.session['clicked']=0
    number=quiz_inst.number_of_questions+1
    context={
        'quiz':quiz_inst,
        'number':number

    }
    
    return render(request, 'users/quizdetail.html',context)
 
@login_required
def thankyou(request):
    request.session['clicked']=0
    return render(request,'users/ThankYouPage.html')    
@login_required
def quizresults(request):
    request.session['clicked']=0
    quizzes=Quiz.objects.all()
    context={
        'quiz':quizzes
    }   
    return render(request,'users/quizresults.html',context)
def credits(request):
    return render(request,'users/credit.html')

        

