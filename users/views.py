from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm,QuizForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Quiz,Questions,Answers,UserAnswer
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model




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
'''def questions(request,pk):

    quizzes = Quiz.objects.get(pk=pk)
    #questions=Questions.objects.all()
    ques=[]
    
    for q in quizzes.get_questions():
        
        ans=[]#to make sure after every question, we reset the answers 
        for a in q.get_answers():
            ans.append(a.text)
        ques.append({str(q):ans})


    context={'quizzes':quizzes,
             'questions':ques
             }
    return render(request,'users/Questions.html',context)


# views.py'''



#@login_required
'''def questions(request, pk):
    quizzes = Quiz.objects.get(pk=pk)
    questions_list = []

    for q in quizzes.get_questions():
        answer=[]
        for a in q.get_answers():
            answer.append(a.text)
        questions_list.append({str(q):answer})

    context={'data':questions_list}
    return JsonResponse(context)'''

                    
    #else:
        #return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

#from django.shortcuts import get_object_or_404

'''@login_required
def quiz_view(request, pk):
    try:
        current_quiz = Quiz.objects.get(pk=pk, user=request.user)
        next_quiz = Quiz.objects.filter(user=request.user, sequence=current_quiz.sequence + 1).first()
    except Quiz.DoesNotExist:
        return HttpResponse("Quiz not found.", status=404)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=current_quiz)
        if form.is_valid():
            selected_answer = form.cleaned_data['selected_option']
            current_quiz.selected_answer = selected_answer
            current_quiz.save()
            # Redirect to the next question or success page

            if next_quiz:
                return redirect('quiz', pk=next_quiz.pk)
            else:
                return HttpResponse("You have completed the quiz!")
    else:
        form = QuizForm(instance=current_quiz)

    context = {
        'quiz': current_quiz,
        'form': form,
    }
    return render(request, 'users/quiz.html', context)'''
'''@login_required
def questions(request, pk):
    try:
        question_instance = Questions.objects.get(pk=pk)
        
    except Questions.DoesNotExist:
        # Handle the case when the question doesn't exist
        return redirect('quiz_not_found')  # Redirect to an appropriate view
     
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=question_instance)
        if form.is_valid():

            selected_answer_text = form.cleaned_data['selected_answer']
            selected_answer = Answers.objects.get(question=question_instance, text=selected_answer_text)
            user_answer=form.save(commit=False)
            # Create a UserAnswer instance to track the selected answer
            
            user_answer,created = UserAnswer.objects.get_or_create(
            
            user=request.user,
            question=question_instance
            )
            #user_answer = UserAnswer.objects.create(user=request.user, question=question_instance, answer=selected_answer)
            user_answer.answer = selected_answer
            user_answer.save()
            # Save the form after creating the UserAnswer instance
            
            
            # Redirect to the next question or a thank you page
            #return redirect('next_question_view')
    else:
        form = QuizForm(instance=question_instance)
    context={'form':form,'question':question_instance}
    
    return render(request, 'users/quiz.html', context)'''
@login_required
def quizdetailview(request,pk):
    quiz_instance=Quiz.objects.get(pk=pk)
    context={'quizdetail':quiz_instance}
    return render(request,'users/quizdetail.html',context)

@login_required
def quizquestions(request, pk):
    try:
        quiz_instance = Quiz.objects.get(pk=pk)
        
    except Quiz.DoesNotExist:
        # Handle the case when the question doesn't exist
        return redirect('quiz_not_found')  # Redirect to an appropriate view
     
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz_instance)
        if form.is_valid():
            
            #selected_answer = form.cleaned_data[selected_answer]
            selected_answer_id=request.POST.get("selected_answer")
            
            selected_answer=Answers.objects.get(id=selected_answer_id)
            question_answered=selected_answer.question
            user_answer=form.save(commit=False)
            # Create a UserAnswer instance to track the selected answer
            user_answer,created = UserAnswer.objects.get_or_create(
            user=request.user,
            question=question_answered
            )
            #user_answer = UserAnswer.objects.create(user=request.user, question=question_instance, answer=selected_answer)
            user_answer.quiz=quiz_instance
            user_answer.answer = selected_answer
            user_answer.save()
            # Save the form after creating the UserAnswer instance
            
            
            # Redirect to the next question or a thank you page
            #return redirect('next_question_view')
    else:
        form = QuizForm(instance=quiz_instance)
    context={'form':form,'quiz':quiz_instance}
    
    return render(request, 'users/quiz.html', context)
def results(request):
    User = get_user_model()
    users=User.objects.all()
    quizs=Quiz.objects.all()
    for user in users:
        for quiz in quizs:
            for question in quiz.get_questions():
                


        

