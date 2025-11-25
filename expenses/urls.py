from django.urls import path, include

urlpatterns = [
    path('', include('expenses.general.urls')),
    path('', include('expenses.groups.urls')),
    path('', include('expenses.expense_module.urls')),
]
