from django.urls import path
from . import views

urlpatterns = [
    path('create-group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/balances/', views.balance_summary, name='balance_summary'),
    path('api/group/<int:group_id>/balances/', views.api_group_balances, name='api_group_balances'),
]