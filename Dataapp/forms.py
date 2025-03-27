from django import forms
from .models import *
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class UserForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model=User
        fields= ['name', 'gender', 'contact_no']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Login
        fields = ['email', 'password']

class BussinesForm(forms.ModelForm):
    class Meta:
        model=Bussines
        fields=['bussines_name','bussines_category','address','district','city','contact_no']

class login_form(forms.Form):
    email=forms.EmailField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())

class EmailForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email']

class SurveyForm(forms.ModelForm):
    class Meta:
        model=Survey
        fields=['question','option1','option2','option3','option4']

class UserSurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(UserSurveyForm,self).__init__(*args, **kwargs)
        self.fields['option']=forms.ChoiceField(choices=[
            ('option1',question.option1),
            ('option2',question.option2),
            ('option3',question.option3),

            ('option4',question.option4),
        ],widget=forms.RadioSelect)
    class Meta:
        model=UserSurvey
        fields=['option']