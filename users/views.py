from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm, ProfileUpdateForm,QuizForm
from django.contrib.auth.decorators import login_required
from .models import Profile,Quiz,Questions,Answers
from django.http import HttpResponse
from django.http import JsonResponse



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




def Quizlist(request):
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



@login_required
def questions(request, pk):
    quizzes = Quiz.objects.get(pk=pk)
    questions_list = []

    for q in quizzes.get_questions():
        answer=[]
        for a in q.get_answers():
            answer.append(a.text)
        questions_list.append({str(q):answer})

    context={'data':questions_list}
    return JsonResponse(context)

                    
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



