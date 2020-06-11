from django.urls import path
from . import views
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='homepage'),
    path('admin/', admin.site.urls),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutUser, name='logout'),
]