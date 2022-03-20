import email
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField,AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Profile, UserManager

#For using customized User model, we need a funtion : get_user_model
User = get_user_model()

class UserRegisterationForm(forms.ModelForm):
    # User Registeration Form
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder' : _('Email address'),
                'required': 'True'
            }
        )
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder' : _('Password'),
                'required' : 'True'
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )
    class Meta:
        model= User
        fields= ('email',)
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self,commit=True):
        user = super(UserRegisterationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        # UserManager.create_superuser()
        if commit:
            user.save()
            print("user has been saved.")
        return user

class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder' : _('Email address'),
                'required': 'True'
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        widget= forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True'
            }
        )
    )
    class Meta:
        model = User
        fields=('email',)
        
        def is_authenticate(self):
            user = authenticate(email=self.email,password= self.password)
            if user is not None:
                return print("authenticate is O")
            else:
                return print("authenticate is X")


class UserChangeForm(forms.ModelForm):
    # Password change form
    password = ReadOnlyPasswordHashField(
        label=_("Password")
    )
    class Meta:
        model=User
        fields=('email','password',)

    def clean_password(self):
        return self.initial["password"]