from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Answers,Questions,Quiz
from django.forms import ModelForm



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),  # Use PasswordInput widget for password1 field
            'password2': forms.PasswordInput(),  # Use PasswordInput widget for password2 field
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'New Password'
        self.fields['password2'].label = 'Confirm New Password'
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


'''class QuizForm(forms.ModelForm):
    
    selected_option = forms.ChoiceField(
        choices=[('option1','Option 1'), ('option2','Option 2'), ('option3','Option 3'), ('option4','Option 4')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Quiz
        fields = ['selected_option']'''

# forms.py


# forms.py


'''class QuizForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['text']
        exclude = ["text"]  # Add other fields as needed
        
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        
        
        question_instance = kwargs.get('instance')
        
        
        answers = question_instance.get_answers()
        
        
        answer_choices = [(answer.text, answer.text) for answer in answers]
        
        
        self.fields['selected_answer'] = forms.ChoiceField(
            label="Select the correct answer",
            choices=answer_choices,
            widget=forms.RadioSelect
        )'''
class QuizForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['text']
        exclude = ["text"]  # Add other fields as needed
        
    selected_answer = forms.ChoiceField(
        label="",
        choices=[],  # We'll update choices dynamically
        widget=forms.RadioSelect
    )
    
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        
        question_instance = kwargs.get('instance')
        
        answer_choices = []
        
        answers = question_instance.get_answers()
        answer_choices=[(answer.id, answer.text) for answer in answers]
            
        self.fields["selected_answer"] = forms.ChoiceField(
                label='select the correct option',
                choices=answer_choices,
                widget=forms.RadioSelect
            )
            
            
                       
    
    

                    

