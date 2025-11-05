from django.contrib import admin
from .models import Member, Expense, Group

admin.site.register(Member)  # Register Member model
admin.site.register(Expense)  # Register Expense model
admin.site.register(Group)  # Register Group model
