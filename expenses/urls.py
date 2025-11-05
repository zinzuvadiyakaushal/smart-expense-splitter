from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('create-group/', views.create_group, name='create_group'),  # Create group
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),  # Group details
    path('group/<int:group_id>/add-expense/', views.add_expense, name='add_expense'),  # Add expense
    path('group/<int:group_id>/balances/', views.balance_summary, name='balance_summary'),  # Balance summary
]
