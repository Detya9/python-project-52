from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'form.html'
    success_message = _("You were logged in")
    extra_context = {'title': _('Login'), 'button_name': _('Log in')}


class CustomLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You were logged out'))
        return super().dispatch(request, *args, **kwargs)

