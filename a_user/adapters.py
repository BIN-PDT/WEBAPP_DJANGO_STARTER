from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.shortcuts import resolve_url


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return resolve_url("profile-onboarding")


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get("email")

        if not email:
            return None

        if sociallogin.is_existing:
            user = sociallogin.user
            email_address, _ = EmailAddress.objects.get_or_create(
                user=user, email=email
            )
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
        else:
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                sociallogin.connect(request, existing_user)

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        email_address, _ = EmailAddress.objects.get_or_create(
            user=user, email=user.email
        )
        if not email_address.verified:
            email_address.verified = True
            email_address.save()

        return user
