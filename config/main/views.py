from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.signing import BadSignature

from .models import AdvUser
from .forms import ProfileEditeForm, RegisterForm
from .utilities import signer


class AdvLoginView(LoginView):
    template_name = "main/login.html"


class AdvLogoutView(LogoutView):
    pass


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "send_messages",
    )
    template_name = "main/profile_edit.html"
    from_class = ProfileEditeForm
    success_url = reverse_lazy("main:profile")
    success_message = "Данные успешно изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class AdvPasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = "main/password_edit.html"
    success_url = reverse_lazy("main:profile")
    success_message = "Ваш пароль успешно изменён"


class AdvRegisterView(CreateView):
    model = AdvUser
    template_name = "main/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("main:register_done")


class AdvRegisterDoneView(TemplateView):
    template_name = "main/register_done.html"


class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = "main/profile_delete.html"
    success_url = reverse_lazy("main:index")
    success_message = "Пользователь успешно удалён"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, "main/activation_failed.html")
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = "main/activation_done_earlier.html"
    else:
        template = "main/activation_done.html"
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


def index(request):
    return render(request, "main/index.html")


def other(request, page):
    try:
        template = get_template("main/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    return render(request, "main/profile.html")
