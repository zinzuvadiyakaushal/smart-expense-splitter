from django import forms
from ..models import Group

class GroupForm(forms.ModelForm):
    members_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter member names (one per line or comma-separated)\nExample:\nJohn Doe\nJane Smith\nBob Johnson',
            'rows': 4,
            'style': 'resize: vertical;'
        }),
        help_text='Enter member names for this group. You can write any names - they will be added as group members. One name per line or separated by commas.'
    )

    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter group name'}),
        }