from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'profile_pic', 'cover'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_common_styles(self.fields)
        self.fields['profile_pic'].widget.attrs.update({
            'id': 'profile'
        })
        self.fields['cover'].widget.attrs.update({
            'id': 'cover'
        })

def add_common_styles(fields):
    for field_name, field in fields.items():
        field.widget.attrs.update({
            'placeholder': field.label
        })

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_common_styles(self.fields)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_pic', 'cover']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_common_styles(self.fields)
        self.fields['profile_pic'].widget.attrs.update({
            'id': 'profile'
        })
        self.fields['cover'].widget.attrs.update({
            'id': 'cover'
        })