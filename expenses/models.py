from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile', null=True, blank=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(Member, related_name='groups')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (by {self.creator.username})"

    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())

    def get_member_count(self):
        return self.members.count()

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('shopping', 'Shopping'),
        ('bills', 'Bills'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_expenses')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    participants = models.ManyToManyField(Member, related_name='expenses', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount} (by {self.added_by.username})"

    def get_split_amount(self):
        participant_count = self.participants.count()
        if participant_count > 0:
            return self.amount / participant_count
        return 0

    class Meta:
        ordering = ['-date']
