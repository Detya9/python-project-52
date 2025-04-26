from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import AuthorAccessMixin, CustomLoginRequiredMixin

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(CustomLoginRequiredMixin, FilterView):
    model = Task
    ordering = 'id'
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_info.html'
    context_object_name = 'task'


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin,
                     CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('task_list')
    success_message = _("Task was successfully created")
    extra_context = {'title': _('Create task'), 'button_name': _('Create')}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('task_list')
    success_message = _("Task was successfully updated")
    extra_context = {'title': _('Update task'), 'button_name': _('Update')}


class TaskDeleteView(CustomLoginRequiredMixin, AuthorAccessMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('task_list')
    success_message = _("Task was successfully deleted")
    extra_context = {'title': _('Delete task')}

