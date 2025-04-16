from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("You are not logged in!"
                                      " Please sign in."))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomUserPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user == self.get_object()

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            messages.error(request, _("You don't have permission"
                                      " to modify another user."))
            return redirect(reverse_lazy('users_list'))
        return super().dispatch(request, *args, **kwargs)

