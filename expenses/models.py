from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    # Member model to represent users in groups
    name = models.CharField(max_length=100)  # Simple name field
    email = models.EmailField(unique=True, blank=True, null=True)  # Email, optional
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')  # Link to Django User

    def __str__(self):
        return self.name  # Display name in admin

class Group(models.Model):
    # Group model for expense groups
    name = models.CharField(max_length=100)  # Group name
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')  # User who created the group
    members = models.ManyToManyField(Member, related_name='groups')  # Members in the group
    created_date = models.DateTimeField(auto_now_add=True)  # Auto-set creation date

    def __str__(self):
        return f"{self.name} (by {self.creator.username})"  # Display name and creator

    def get_total_expenses(self):
        # Calculate total expenses for the group
        return sum(expense.amount for expense in self.expenses.all())

    def get_member_count(self):
        # Get number of members
        return self.members.count()

class Expense(models.Model):
    # Expense model for tracking expenses
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('shopping', 'Shopping'),
        ('bills', 'Bills'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=150)  # Expense title
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Use Decimal for precise money calculations
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # Category
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_expenses')  # User who added the expense
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')  # Link to group
    participants = models.ManyToManyField(Member, related_name='expenses', blank=True)  # Who participated
    date = models.DateTimeField(auto_now_add=True)  # Auto-set date
    description = models.TextField(blank=True, null=True)  # Optional description for more details

    def __str__(self):
        return f"{self.title} - ₹{self.amount} (by {self.added_by.username})"  # Display title, amount, and adder

    def get_split_amount(self):
        # Calculate equal split amount per participant
        participant_count = self.participants.count()
        if participant_count > 0:
            return self.amount / participant_count
        return 0

    class Meta:
        ordering = ['-date']  # Order expenses by date descending
