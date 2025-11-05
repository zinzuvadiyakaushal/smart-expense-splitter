from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .models import Group, Expense, Member
from .forms import GroupForm, ExpenseForm
from .utils import calculate_balances

@login_required
def home(request):
    # Home view: Dashboard showing user's groups
    groups = Group.objects.filter(creator=request.user)  # Get groups created by user
    return render(request, 'expenses/home.html', {'groups': groups})  # Render home template

@login_required
def create_group(request):
    # View to create a new group
    if request.method == 'POST':
        form = GroupForm(request.POST)  # Get form data
        if form.is_valid():
            group = form.save(commit=False)  # Don't save yet
            group.creator = request.user  # Set creator
            group.save()  # Save group
            form.save_m2m()  # Save many-to-many members
            messages.success(request, 'Group created successfully!')  # Success message
            return redirect('home')  # Redirect to home
    else:
        form = GroupForm()  # Empty form
    return render(request, 'expenses/create_group.html', {'form': form})  # Render form template

@login_required
def group_detail(request, group_id):
    # View to show group details and expenses
    group = get_object_or_404(Group, id=group_id, creator=request.user)  # Get group or 404
    expenses = group.expenses.all()  # Get expenses in group
    return render(request, 'expenses/group_detail.html', {'group': group, 'expenses': expenses})  # Render template

@login_required
def add_expense(request, group_id):
    # View to add expense to a group
    group = get_object_or_404(Group, id=group_id, creator=request.user)  # Get group
    if request.method == 'POST':
        form = ExpenseForm(request.POST)  # Get form data
        if form.is_valid():
            expense = form.save(commit=False)  # Don't save yet
            expense.added_by = request.user  # Set added_by
            expense.group = group  # Set group
            expense.save()  # Save expense
            form.save_m2m()  # Save participants
            messages.success(request, 'Expense added successfully!')  # Success message
            return redirect('group_detail', group_id=group.id)  # Redirect to group detail
    else:
        form = ExpenseForm()  # Empty form
    return render(request, 'expenses/add_expense.html', {'form': form, 'group': group})  # Render template

@login_required
def balance_summary(request, group_id):
    # View to show balance summary for a group
    group = get_object_or_404(Group, id=group_id, creator=request.user)  # Get group
    balances = calculate_balances(group)  # Calculate balances
    return render(request, 'expenses/balance_summary.html', {'group': group, 'balances': balances})  # Render template

def logout_view(request):
    # Custom logout view: Log out user, show message, redirect to login
    logout(request)  # Log out the user
    messages.success(request, 'You have been logged out successfully.')  # Success message
    return redirect('login')  # Redirect to login page
