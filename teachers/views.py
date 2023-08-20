from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import QuestionsForm, OptionsFormSet,UserRegisterForm
from django.contrib.auth.decorators import login_required,user_passes_test

def email_check(user):
    return user.email.endswith('@iiitb.com')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('teacherlogin')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
# Create your views here.

@user_passes_test(email_check)
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionsForm(request.POST)
        options_formset = OptionsFormSet(request.POST, prefix='options')

        if question_form.is_valid() and options_formset.is_valid():
            question = question_form.save()  # Save the question form

            # Set the question instance for each option before saving the options formset
            options = options_formset.save(commit=False)
            for option in options:
                option.question = question
                option.save()

            #return messages.success('Questions saved successfully')  # Redirect to a success page
            
    else:
        question_form = QuestionsForm()
        options_formset = OptionsFormSet(prefix='options')

    context = {'question_form': question_form, 'options_formset': options_formset}
    return render(request, 'teachers/create_question.html', context)


