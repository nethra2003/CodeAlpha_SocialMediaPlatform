from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Choose a username"
            })
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]

        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write something about yourself",
                "rows": 3
            })
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image", "video"]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "What's on your mind?",
                "rows": 3,
                "maxlength": 5000
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/jpeg,image/png,image/gif,image/webp"
            }),
            "video": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "video/mp4,video/webm,video/ogg"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        content = (cleaned_data.get("content") or "").strip()
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")

        if not content and not image and not video:
            raise forms.ValidationError(
                "Write something or upload an image or video before posting."
            )

        if image and image.size > 10 * 1024 * 1024:
            self.add_error("image", "Images must be 10 MB or smaller.")

        if video and video.size > 50 * 1024 * 1024:
            self.add_error("video", "Videos must be 50 MB or smaller.")

        if image and video:
            raise forms.ValidationError(
                "Please upload either an image or a video per post."
            )

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write a comment...",
                "rows": 2
            })
        }