from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .models import User


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, World!")


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('home')
    success_message = _("User was successfully registered")

