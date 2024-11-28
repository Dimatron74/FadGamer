from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Email

class SignupForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('nickname', 'password1', 'password2')

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     if commit:
    #         user.save()
    #         Email.objects.create(user=user, email=self.cleaned_data['email'], is_active=False)
    #     return user
