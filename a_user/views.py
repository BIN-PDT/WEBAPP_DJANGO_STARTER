from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import ProfileEditForm, AccountEmailChangeForm


def profile_view(request: HttpRequest, username: str = None):
    if username:
        user = get_object_or_404(User, username=username)
        profile = user.profile
    else:
        user = request.user
        if user.is_authenticated:
            profile = user.profile
        else:
            redirect_url = f"{reverse("account_login")}?next={reverse("profile")}"
            return redirect(redirect_url)

    context = {"profile": profile}
    return render(request, "a_user/profile.html", context)


@login_required
def profile_edit_view(request: HttpRequest):
    profile = request.user.profile
    form = ProfileEditForm(instance=profile)

    if request.method == "POST":
        form = ProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("profile")

    is_onboarding = request.path == reverse("profile-onboarding")
    context = {"form": form, "is_onboarding": is_onboarding}
    return render(request, "a_user/profile_edit.html", context)


@login_required
def profile_settings_view(request: HttpRequest):
    user = request.user
    used_providers = [e.provider for e in user.socialaccount_set.all()]
    form = AccountEmailChangeForm(instance=user)

    if request.method == "POST":
        form = AccountEmailChangeForm(instance=user, data=request.POST)

        if form.is_valid():
            if (
                User.objects.filter(email=form.cleaned_data["email"])
                .exclude(id=user.id)
                .exists()
            ):
                messages.error(request, "Email is already in use!")
            else:
                form.save()
                send_email_confirmation(request, user)
        else:
            messages.error(request, "Invalid form credentials!")

        return redirect("profile-settings")

    context = {"form": form, "used_providers": used_providers}
    return render(request, "a_user/profile_settings.html", context)


@login_required
def profile_delete_view(request: HttpRequest):
    user = request.user

    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, what a pity!")
        return redirect("home")

    return render(request, "a_user/profile_delete.html")


@login_required
def account_verify_email(request: HttpRequest):
    send_email_confirmation(request, request.user)
    return redirect("profile-settings")


@login_required
def link_social_account(request: HttpRequest, provider: str):
    if SocialAccount.objects.filter(user=request.user, provider=provider).exists():
        messages.error(request, f"Your account was linked to {provider.upper()}!")
        return redirect("profile-settings")
    return redirect(f"/accounts/{provider}/login/")
