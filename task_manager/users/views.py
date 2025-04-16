from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import (
    CustomLoginRequiredMixin,
    CustomUserPassesTestMixin,
)

from .forms import CustomUserChangeForm, CustomUserCreationForm
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
    success_url = reverse_lazy('login')
    success_message = _("User was successfully registered")
    extra_context = {'title': _('Registration'), 'button_name': _('Register')}


class UserUpdateView(CustomLoginRequiredMixin, CustomUserPassesTestMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'form.html'
    success_url = reverse_lazy('users_list')
    success_message = _("User was successfully updated")
    extra_context = {'title': _('Update user'), 'button_name': _('Update')}


class UserDeleteView(CustomLoginRequiredMixin, CustomUserPassesTestMixin,
                     SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _("User was successfully deleted")
    extra_context = {'title': _('Delete user')}

