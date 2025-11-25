from django.urls import path
from . import views

urlpatterns = [
    path('group/<int:group_id>/add-expense/', views.add_expense, name='add_expense'),
]