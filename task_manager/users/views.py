from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .models import User


class UserListView(ListView):
    model = User
    ordering = 'id'
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')
    success_message = _("User was successfully registered")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Registration')
        context['button_name'] = _('Register')
        return context

