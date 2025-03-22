from django import forms
from .models import User, Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        labels = {"image": "", "realname": "", "biography": ""}
        widgets = {
            "image": forms.FileInput(
                {
                    "accept": "image/*",
                    "class": "!px-5 py-0",
                }
            ),
            "realname": forms.TextInput(
                {
                    "placeholder": "Add name",
                }
            ),
            "biography": forms.Textarea(
                {
                    "rows": 3,
                    "placeholder": "Add biography",
                }
            ),
        }


class AccountEmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        labels = {"email": ""}
        widgets = {"email": forms.EmailInput()}
