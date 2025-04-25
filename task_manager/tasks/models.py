from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'), blank=True,
                                   null=True)
    status = models.ForeignKey(Status, verbose_name=_('Status'),
                               on_delete=models.PROTECT,
                               related_name='status_tasks')
    author = models.ForeignKey(User, verbose_name=_('Author'),
                               on_delete=models.PROTECT,
                               related_name='self_tasks')
    executor = models.ForeignKey(User, verbose_name=_('Executor'),
                                 on_delete=models.PROTECT, null=True,
                                 related_name='tasks', blank=True)
    created_at = models.DateTimeField(verbose_name=_('Creation date'),
                                      auto_now_add=True)

    def __str__(self):
        return self.name

