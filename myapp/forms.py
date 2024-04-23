from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StudentSignUpForm(UserCreationForm):
    student_name = forms.CharField(max_length=100, help_text='Enter your full name')
    registration_number = forms.CharField(max_length=50)
    roll_number = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'student_name', 'registration_number', 'roll_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['student_name']
        user.save()
        return user
