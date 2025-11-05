from django import forms
from .models import Group, Expense, Member

class GroupForm(forms.ModelForm):
    # Form for creating a group
    class Meta:
        model = Group
        fields = ['name', 'members']  # Fields to include
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter group name'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ExpenseForm(forms.ModelForm):
    # Form for adding an expense
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'participants']  # Fields to include
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter expense title'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'participants': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
