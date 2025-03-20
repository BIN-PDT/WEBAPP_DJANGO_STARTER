from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import resolve_url, redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return resolve_url("profile-onboarding")


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if not sociallogin.is_existing:
            email_addresses = [e.email for e in sociallogin.email_addresses]
            if EmailAddress.objects.filter(email__in=email_addresses).exists():
                messages.error(request, "Email is already linked to another account.")
                raise ImmediateHttpResponse(redirect("account_login"))
