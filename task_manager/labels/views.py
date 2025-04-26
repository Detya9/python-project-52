from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import CustomLoginRequiredMixin, ErrorCatcherMixin

from .forms import LabelForm
from .models import Label


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    ordering = 'id'
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin,
                      CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('label_list')
    success_message = _("Label was successfully created")
    extra_context = {'title': _('Create label'), 'button_name': _('Create')}


class LabelUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin,
                      UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('label_list')
    success_message = _("Label was successfully updated")
    extra_context = {'title': _('Update label'), 'button_name': _('Update')}


class LabelDeleteView(CustomLoginRequiredMixin, ErrorCatcherMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = _("Label was successfully deleted")
    extra_context = {'title': _('Delete label')}
    error_message = _("Label can't be deleted, because it is in use")
    error_redirect_name = reverse_lazy('label_list')

