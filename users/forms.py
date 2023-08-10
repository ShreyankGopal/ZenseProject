from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Answers



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


class QuizForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)

        if questions:
            for question_dict in questions:
                for question, answers in question_dict.items():
                    question_id = question.id
                    choices = [(answer.id, answer.text) for answer in answers]
                    self.fields[f'question_{question_id}'] = forms.ChoiceField(
                        choices=choices,
                        widget=forms.RadioSelect,
                        required=True,
                    )

                    

