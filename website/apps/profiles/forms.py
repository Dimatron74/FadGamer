from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Email, UserEmail



class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('nickname', 'email')



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Email.objects.filter(email=email).exists():
            print("This email is already in use.")
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        confirm_password = self.cleaned_data.get('password2')
        if password and confirm_password and password != confirm_password:
            print("Passwords do not match.")
            raise forms.ValidationError("Passwords do not match.")
        print("password ok")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            email_instance, created = Email.objects.get_or_create(email=self.cleaned_data['email'])
            UserEmail.objects.create(user=user, email=email_instance, is_active=True, is_confirmed=False)
        return user