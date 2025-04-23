from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import CustomLoginRequiredMixin

from .forms import StatusForm
from .models import Status


class StatusListView(CustomLoginRequiredMixin, ListView):
    model = Status
    ordering = 'id'
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginRequiredMixin, SuccessMessageMixin,
                       CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status was successfully created")
    extra_context = {'title': _('Create status'), 'button_name': _('Create')}


class StatusUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status was successfully updated")
    extra_context = {'title': _('Update status'), 'button_name': _('Update')}


class StatusDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin,
                       DeleteView):
    model = Status
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('status_list')
    success_message = _("Status was successfully deleted")
    extra_context = {'title': _('Delete status')}

