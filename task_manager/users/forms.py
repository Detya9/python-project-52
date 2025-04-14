from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name',) + UserCreationForm.Meta.fields


# class CustomUserChangeForm(UserChangeForm):
    # class Meta(UserChangeForm.Meta):
        # model = User
        # fields = UserChangeForm.Meta.fields + ('first_name', 'last_name',)

