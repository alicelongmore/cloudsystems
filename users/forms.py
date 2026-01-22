from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import SetPasswordForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'city', 'country', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }
        
class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exist.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("new_password1")
        pw2 = cleaned_data.get("new_password2")
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['new_password1']
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return user