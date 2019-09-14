from django.contrib import admin
from django.urls import path
from user import views

app_name = 'user'

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns = [
    # path('user_settings/', views.UserSettingsDetailView.as_view(), name='user_settings-detail'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('user_settings/<int:pk>/update/', views.UserSettingsUpdate.as_view(), name='user_settings_update'),
]
