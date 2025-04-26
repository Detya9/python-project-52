from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name=_('Name'))
    created_at = models.DateTimeField(verbose_name=_('Creation date'),
                                      auto_now_add=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.task_set.exists():
            raise ProtectedError(msg='', protected_objects=self.task_set.all())
        return super().delete()

