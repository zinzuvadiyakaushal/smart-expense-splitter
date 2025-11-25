from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Expense, Group
from ..forms import ExpenseForm

@login_required
def add_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id, creator=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, group=group)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.added_by = request.user
            expense.group = group
            expense.save()

            form.save_m2m()

            if not expense.participants.exists():
                expense.participants.set(group.members.all())

            messages.success(request, 'Expense added successfully!')
            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseForm(group=group)
    return render(request, 'expenses/add_expense.html', {'form': form, 'group': group})