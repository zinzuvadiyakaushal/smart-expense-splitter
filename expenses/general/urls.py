from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('api/admin-activity-feed/', views.api_admin_activity_feed, name='api_admin_activity_feed'),
    path('api/admin-stats/', views.api_admin_stats, name='api_admin_stats'),
]