import django_filters
from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskFilter(django_filters.FilterSet):
    user_tasks = django_filters.BooleanFilter(
        label=_('Only your own tasks'),
        method='get_own_tasks',
        widget=CheckboxInput)

    def get_own_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ('status', 'executor',)

