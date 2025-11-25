from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login
from django.db.models import Sum
from django.http import JsonResponse
from ..models import Group, Expense, Member
from ..forms import SignupForm
from ..utils import calculate_balances

@login_required
def home(request):
    groups = Group.objects.filter(creator=request.user).prefetch_related('members', 'expenses')
    expenses_qs = Expense.objects.filter(group__creator=request.user).select_related('group', 'added_by')

    total_amount = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    total_members = Member.objects.filter(groups__creator=request.user).distinct().count()
    pending_amount = 0
    group_cards = []
    for group in groups:
        group_total = group.get_total_expenses()
        group_percent = (float(group_total) / float(total_amount) * 100) if total_amount else 0
        balances = calculate_balances(group)
        pending_amount += sum(balances.values())
        group_cards.append({
            'group': group,
            'total': group_total,
            'percent': round(group_percent, 2),
            'latest_expense': group.expenses.first(),
            'balances': balances,
        })

    recent_expenses = expenses_qs.order_by('-date')[:5]
    pending_cards = [card for card in group_cards if card['balances']]

    first_group_id = group_cards[0]['group'].id if group_cards else None

    context = {
        'groups': [card['group'] for card in group_cards],
        'group_cards': group_cards,
        'pending_cards': pending_cards,
        'total_amount': total_amount,
        'total_members': total_members,
        'pending_amount': pending_amount,
        'recent_expenses': recent_expenses,
        'first_group_id': first_group_id,
    }
    return render(request, 'expenses/home.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Expense Splitter.')
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def api_dashboard(request):
    groups = Group.objects.filter(creator=request.user)
    expenses_qs = Expense.objects.filter(group__creator=request.user)
    total_amount = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    total_members = Member.objects.filter(groups__creator=request.user).distinct().count()
    pending_amount = 0
    group_data = []
    for group in groups:
        balances = calculate_balances(group)
        pending_amount += sum(balances.values())
        group_data.append({
            'id': group.id,
            'name': group.name,
            'members': group.members.count(),
            'total_spend': float(group.get_total_expenses()),
            'pending_pairs': len(balances),
        })
    recent = [
        {
            'title': exp.title,
            'amount': float(exp.amount),
            'group': exp.group.name,
            'date': exp.date.isoformat(),
        }
        for exp in expenses_qs.order_by('-date')[:5]
    ]
    return JsonResponse({
        'groups': group_data,
        'total_amount': float(total_amount),
        'total_members': total_members,
        'pending_amount': float(pending_amount),
        'recent_expenses': recent,
    })


def api_admin_activity_feed(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    activities = []

    recent_groups = Group.objects.all().order_by('-created_date')[:10]
    for group in recent_groups:
        activities.append({
            'type': 'group',
            'title': f'Group "{group.name}" created',
            'meta': f'Created by {group.creator.username}',
            'timestamp': group.created_date.isoformat(),
            'icon': 'group'
        })

    recent_expenses = Expense.objects.all().select_related('group', 'added_by').order_by('-date')[:10]
    for expense in recent_expenses:
        activities.append({
            'type': 'expense',
            'title': f'Expense "{expense.title}" added',
            'meta': f'₹{expense.amount} in "{expense.group.name}"',
            'timestamp': expense.date.isoformat(),
            'icon': 'expense'
        })

    from django.contrib.auth.models import User
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    for user in recent_users:
        activities.append({
            'type': 'user',
            'title': f'User "{user.username}" registered',
            'meta': f'Email: {user.email}',
            'timestamp': user.date_joined.isoformat(),
            'icon': 'user'
        })

    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    activities = activities[:20]

    return JsonResponse({'activities': activities})


def api_admin_stats(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    total_users = User.objects.count()
    total_groups = Group.objects.count()
    total_expenses = Expense.objects.count()
    total_amount = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_members = Member.objects.count()

    from django.utils import timezone
    from datetime import timedelta

    yesterday = timezone.now() - timedelta(days=1)
    recent_groups = Group.objects.filter(created_date__gte=yesterday).count()
    recent_expenses = Expense.objects.filter(date__gte=yesterday).count()
    recent_users = User.objects.filter(date_joined__gte=yesterday).count()

    return JsonResponse({
        'total_users': total_users,
        'total_groups': total_groups,
        'total_expenses': total_expenses,
        'total_amount': float(total_amount),
        'total_members': total_members,
        'recent_groups': recent_groups,
        'recent_expenses': recent_expenses,
        'recent_users': recent_users,
    })