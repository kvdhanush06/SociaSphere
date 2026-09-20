from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from PIL import Image, UnidentifiedImageError

from .models import Post, Profile


HTTP_URL_VALIDATOR = URLValidator(schemes=("http", "https"))
MAX_PROFILE_IMAGE_BYTES = 5 * 1024 * 1024
MAX_PROFILE_IMAGE_DIMENSION = 4096


def validate_http_url(value):
    if not value:
        return
    try:
        HTTP_URL_VALIDATOR(value)
    except ValidationError as exc:
        raise forms.ValidationError("Enter a valid HTTP or HTTPS URL.") from exc


def validate_profile_image(uploaded_file):
    if not uploaded_file:
        return
    if uploaded_file.size > MAX_PROFILE_IMAGE_BYTES:
        raise forms.ValidationError("Profile images must be 5 MB or smaller.")
    try:
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
        with Image.open(uploaded_file) as checked_image:
            width, height = checked_image.size
            if width > MAX_PROFILE_IMAGE_DIMENSION or height > MAX_PROFILE_IMAGE_DIMENSION:
                raise forms.ValidationError("Profile images must be no larger than 4096×4096 pixels.")
        uploaded_file.seek(0)
    except (UnidentifiedImageError, OSError) as exc:
        raise forms.ValidationError("Upload a valid image file.") from exc


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(
        label="Profile Picture",
        required=False,
        validators=[validate_profile_image],
    )
    profile_bio = forms.CharField(
        label="Profile Bio",
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Profile Bio'}
        ),
    )
    homepage_link = forms.CharField(
        label="",
        required=False,
        max_length=200,
        validators=[validate_http_url],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Website Link'}
        ),
    )
    facebook_link = forms.CharField(
        label="",
        required=False,
        max_length=200,
        validators=[validate_http_url],
        widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}
        ),
    )
    instagram_link = forms.CharField(
        label="",
        required=False,
        max_length=200,
        validators=[validate_http_url],
        widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}
        ),
    )
    linkedin_link = forms.CharField(
        label="",
        required=False,
        max_length=200,
        validators=[validate_http_url],
        widget=forms.URLInput(
            attrs={'class': 'form-control', 'placeholder': 'LinkedIn Link'}
        ),
    )

    class Meta:
        model = Profile
        fields = (
            'profile_image',
            'profile_bio',
            'homepage_link',
            'facebook_link',
            'instagram_link',
            'linkedin_link',
        )


class PostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        max_length=200,
        strip=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Enter Your Post!",
                "class": "form-control",
                "maxlength": 200,
            }
        ),
        label="",
    )

    class Meta:
        model = Post
        exclude = ("user", "likes")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'User Name'}
        )
        self.fields['username'].label = ''
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'}
        )
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm Password'}
        )
        self.fields['password2'].label = ''
