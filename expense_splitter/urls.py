from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expenses.views import logout_view, signup_view
from expenses.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('expenses.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]
