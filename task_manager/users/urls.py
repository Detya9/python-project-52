from django.urls import path

from task_manager.users import views

urlpatterns = [
    path("", views.UserListView.as_view(), name='users_list'),
    path("create/", views.UserCreateView.as_view(), name='registration')   
]

