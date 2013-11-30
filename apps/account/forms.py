#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from apps.account.validators import validate_email_unique
from captcha.fields import CaptchaField


class LoginCaptchaForm(AuthenticationForm):
    captcha = CaptchaField()



class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo Electrónico", validators=[validate_email_unique], widget=forms.TextInput(attrs={'placeholder': 'Email', "class": "form-control"}))
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario', "class": "form-control"}),
        help_text="Requerido. 30 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente."
    )

    def clean_password2(self):
        password2 = self.cleaned_data.get("password2")
        if len(password2) <= 6:
            raise forms.ValidationError("Password must to have more than 8 characters")
        return password2

    class Meta:
        model = User
        fields = ("username", "email",)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    username = forms.CharField(label="* Nombre de usuario", widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control", "autofocus": "true"}))
    first_name = forms.CharField(label="* Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre', "class": "form-control"}))
    last_name = forms.CharField(label="* Apellido", widget=forms.TextInput(attrs={'placeholder': 'Apellido', "class": "form-control"}))
    email = forms.EmailField(label="* Correo Electrónico", required=False, validators=[], widget=forms.TextInput(attrs={'placeholder': 'Email', "class": "form-control", 'type': 'email'}))

    class Meta:
        model = User
        # unique = ('email')
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self):
        print self.cleaned_data["email"]
        user = super(UserForm, self).save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user_obj = self.instance.pk
        except Exception, e:
            user_obj = None
        if user_obj:
            """(updating)"""
            there_is_email = User.objects.exclude(pk=self.instance.pk).filter(email=email).count()
        else:
            """(creating)"""
            there_is_email = User.objects.filter(email=email).count()
        if email and there_is_email:
            from django.core.exceptions import ValidationError
            raise ValidationError('Email duplicado, verifique que otro usuario no tenga este mismo correo.')
        return email