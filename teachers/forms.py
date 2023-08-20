from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Quiz,Questions,Answers,UserAnswer,Results
from django.forms import ModelForm
from django.forms import inlineformset_factory
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
class QuestionsForm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=['text','quiz','correct']
class OptionsForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['text']
        

OptionsFormSet = inlineformset_factory(Questions, Answers, form=OptionsForm, extra=4)
        

