
from django.urls import path
from. import views
app_name = 'wall'
urlpatterns = [
    path("", views.index, name = 'main'),
    path("register", views.register, name = 'register'),
    path("login", views.login, name = 'login'),
    path("wall", views.view_wall, name = 'view_wall'),
    path("create_message", views.create_message, name = 'create_message'),
    path("create_comment", views.create_comment, name = 'create_comment'),
    path("logout", views.logout, name = 'logout'),
]
