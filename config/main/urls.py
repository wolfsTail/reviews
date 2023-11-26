from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .views import *


app_name = "main"

urlpatterns = [
    path("accounts/activate/<str:sign>/", user_activate, name="activate"),
    path("account/register/done/", AdvRegisterDoneView.as_view(), name="register_done"),
    path("account/register/", AdvRegisterView.as_view(), name="register"),
    path("accounts/logout/", AdvLogoutView.as_view(), name="logout"),
    path(
        "accounts/password/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="main/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password/reset/complete/",
        PasswordResetConfirmView.as_view(
            template_name="main/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # to do
    path(
        "accounts/password/reset/done",
        PasswordResetView.as_view(
            template_name="main/password_reset.html",
            email_template_name="main/password_reset_email.html",
            success_url=reverse_lazy("main:password_reset_done"),
        ),
        name="password_reset",
    ),
    # near good!
    path(
        "accounts/password/reset/done/",
        PasswordResetView.as_view(template_name="main/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "accounts/password/edit/", AdvPasswordEditView.as_view(), name="password_edit"
    ),
    path(
        "accounts/profile/delete/", ProfileDeleteView.as_view(), name="profile_delete"
    ),
    path("accounts/profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("accounts/profile/", profile, name="profile"),
    path("accounts/login/", AdvLoginView.as_view(), name="login"),
    path("<str:page>/", other, name="other"),
    path("", index, name="index"),
]
