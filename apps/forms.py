from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import ModelForm

from .models import User, Post


class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user with fields for first name, last name, and an optional avatar.
    Methods:
        save(self, commit=True): Saves the user with the provided data, setting the password and committing to the database if specified.
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'avatar', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    '''
    Custom login form extending Django's AuthenticationForm to validate the username and password.
    Methods:
        clean_password: Custom method to validate the password by checking against the user's stored password in the database.

    '''

    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise ValidationError('Please check Username or password !')
        return password


class EditProfile(ModelForm):
    """
    Saves the edited user profile to the database after creating a new user instance.

    Attributes:
        self: The EditProfile instance.

    Returns:
        None
    """

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'email', 'phone',)

    @atomic
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            phone=self.cleaned_data.get('phone'),
        )
        user.set_password(self.cleaned_data.get('password'))
        user.save()


class PostForm(ModelForm):
    """
    A form for creating or updating a post with fields for title and content.
    Note:
        This form is used for creating or updating post instances.
    """

    class Meta:
        model = Post
        fields = ['title', 'content', ]
        widgets = {
            'content': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class UserForm(ModelForm):
    '''
    ModelForm for creating and updating user information.
    '''

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'avatar')
