from django.urls import path
from .views import TaskView, RegisterView, LoginView, UserView, LogoutView

urlpatterns=[
    path('task/',TaskView.as_view(),name='task_list'),
    path('task/<int:id>',TaskView.as_view(),name='task_process'),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view())
]