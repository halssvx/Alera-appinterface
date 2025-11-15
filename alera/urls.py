from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard),
    path("log/", views.log_glucose),
    path("api/glucose/", views.glucose_series),

    path("login/", auth_views.LoginView.as_view(template_name="login.html")),
    path("logout/", auth_views.LogoutView.as_view()),
    path("register/", views.register),
]
