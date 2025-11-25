from django import forms
from ..models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'participants']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter expense title'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount', 'step': '0.01', 'min': '0'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'participants': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if group is not None:
            members = group.members.all()
            self.fields['participants'].queryset = members
            self.fields['participants'].required = True
            if members.exists():
                member_count = members.count()
                self.fields['participants'].widget.attrs.update({
                    'class': 'form-select',
                    'size': min(member_count, 8),
                    'style': 'min-height: 120px;'
                })
                self.fields['participants'].help_text = f'Select participants from the {member_count} group members. Hold Ctrl/Cmd to select multiple.'
            else:
                self.fields['participants'].widget.attrs.update({
                    'class': 'form-select',
                })
                self.fields['participants'].help_text = 'No members in this group.'