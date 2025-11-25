from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from ..models import Group, Member
from ..forms import GroupForm
from ..utils import calculate_balances

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()

            members_text = form.cleaned_data.get('members_text', '')
            if members_text:
                member_names = [name.strip() for name in members_text.replace('\n', ',').split(',') if name.strip()]

                for name in member_names:
                    member, created = Member.objects.get_or_create(
                        name=name,
                        defaults={'user': None}
                    )
                    group.members.add(member)

            messages.success(request, 'Group created successfully!')
            return redirect('home')
    else:
        form = GroupForm()
    return render(request, 'expenses/create_group.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, creator=request.user)
    expenses = group.expenses.all()
    return render(request, 'expenses/group_detail.html', {'group': group, 'expenses': expenses})

@login_required
def balance_summary(request, group_id):
    group = get_object_or_404(Group, id=group_id, creator=request.user)
    balances = calculate_balances(group)
    return render(request, 'expenses/balance_summary.html', {'group': group, 'balances': balances})

@login_required
def api_group_balances(request, group_id):
    group = get_object_or_404(Group, id=group_id, creator=request.user)
    balances = calculate_balances(group)
    data = [
        {
            'from_member': source,
            'to_member': target,
            'amount': float(amount),
        }
        for (source, target), amount in balances.items()
    ]
    return JsonResponse({'group': group.name, 'balances': data})