from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from . import views
app_name = 'accounts'

urlpatterns = [
    path('', views.indexView, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('main/', views.mainView, name='main')
]
