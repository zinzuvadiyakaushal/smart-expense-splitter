from django.contrib import admin
from django.db.models import Sum, Count, Avg
from django.utils.html import format_html
from django.urls import reverse
from django.db.models.functions import TruncMonth
from django.db.models import F
from .models import Member, Expense, Group
from .utils import calculate_balances

class MemberInline(admin.TabularInline):
    model = Group.members.through
    extra = 0
    autocomplete_fields = ['member']
    verbose_name = "Group Member"
    verbose_name_plural = "Group Members"

class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0
    readonly_fields = ('title', 'amount', 'added_by', 'date', 'participants_count')
    can_delete = False
    show_change_link = True

    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = "Participants"

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'groups_count', 'total_expenses', 'net_balance')
    list_filter = ('user', 'groups')
    search_fields = ('name', 'email', 'user__username')

    def groups_count(self, obj):
        return obj.groups.count()
    groups_count.short_description = "Groups"

    def total_expenses(self, obj):
        total = Expense.objects.filter(participants=obj).aggregate(Sum('amount'))['amount__sum'] or 0
        return f"₹{total:.2f}"
    total_expenses.short_description = "Total Expenses"

    def net_balance(self, obj):
        # Calculate net balance across all groups
        net = 0
        for group in obj.groups.all():
            balances = calculate_balances(group)
            for (debtor, creditor), amount in balances.items():
                if debtor == obj.name:
                    net -= amount
                elif creditor == obj.name:
                    net += amount
        return f"₹{net:.2f}"
    net_balance.short_description = "Net Balance"

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'group_link', 'added_by', 'amount_colored', 'category_badge', 'participants_count', 'date', 'split_amount')
    list_filter = ('category', 'group', 'added_by', 'date')
    search_fields = ('title', 'description', 'group__name')
    readonly_fields = ('date',)
    date_hierarchy = 'date'

    def group_link(self, obj):
        url = reverse('admin:expenses_group_change', args=[obj.group.id])
        return format_html('<a href="{}" style="color: #0d6efd; font-weight: 600;">{}</a>', url, obj.group.name)
    group_link.short_description = "Group"
    group_link.admin_order_field = 'group__name'

    def amount_colored(self, obj):
        color = "#198754" if obj.amount < 1000 else "#fd7e14" if obj.amount < 5000 else "#dc3545"
        html = f'<span style="color: {color}; font-weight: 700; font-size: 1.1em;">₹{float(obj.amount):.2f}</span>'
        return format_html(html)
    amount_colored.short_description = "Amount"
    amount_colored.admin_order_field = 'amount'

    def category_badge(self, obj):
        colors = {
            'food': '#198754',
            'travel': '#0d6efd',
            'shopping': '#fd7e14',
            'bills': '#dc3545',
            'entertainment': '#6f42c1',
            'other': '#6c757d'
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html('<span style="background: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8em; font-weight: 600;">{}</span>', color, obj.get_category_display())
    category_badge.short_description = "Category"

    def participants_count(self, obj):
        count = obj.participants.count()
        return format_html('<span style="background: #e9ecef; color: #495057; padding: 2px 6px; border-radius: 10px; font-size: 0.9em;">{} 👥</span>', count)
    participants_count.short_description = "Participants"

    def split_amount(self, obj):
        split = obj.get_split_amount()
        return f"₹{split:.2f}"
    split_amount.short_description = "Per Person"

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator_link', 'members_count', 'expenses_count', 'total_amount', 'balance_status', 'created_date')
    list_filter = ('creator', 'created_date')
    search_fields = ('name', 'creator__username', 'members__name')
    readonly_fields = ('created_date',)
    date_hierarchy = 'created_date'
    inlines = [MemberInline, ExpenseInline]

    def creator_link(self, obj):
        return format_html('<span style="color: #4b5563; font-weight: 600;">{}</span>', obj.creator.username)
    creator_link.short_description = "Creator"
    creator_link.admin_order_field = 'creator__username'

    def members_count(self, obj):
        count = obj.members.count()
        return format_html('<span style="background: #e7f3ff; color: #0d6efd; padding: 3px 8px; border-radius: 12px; font-weight: 600;">{} 👤</span>', count)
    members_count.short_description = "Members"

    def expenses_count(self, obj):
        count = obj.expenses.count()
        return format_html('<span style="background: #f8f9fa; color: #6c757d; padding: 3px 8px; border-radius: 12px; font-weight: 600;">{} 💰</span>', count)
    expenses_count.short_description = "Expenses"

    def total_amount(self, obj):
        total = obj.get_total_expenses()
        html = f'<span style="color: #198754; font-weight: 700; font-size: 1.1em;">₹{float(total):.2f}</span>'
        return format_html(html)
    total_amount.short_description = "Total Spent"

    def balance_status(self, obj):
        balances = calculate_balances(obj)
        if not balances:
            html = '<span style="background: #d1ecf1; color: #0c5460; padding: 3px 8px; border-radius: 12px; font-size: 0.9em;">✅ Balanced</span>'
            return format_html(html)

        total_pending = sum(balances.values())
        html = f'<span style="background: #fff3cd; color: #856404; padding: 3px 8px; border-radius: 12px; font-size: 0.9em;">⚠️ ₹{float(total_pending):.2f} pending</span>'
        return format_html(html)
    balance_status.short_description = "Status"

# Professional Admin Site with Real Data
class ExpenseSplitterAdminSite(admin.AdminSite):
    site_header = "Expense Splitter Admin"
    site_title = "Expense Splitter Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        from django.utils import timezone
        from django.db.models import Sum

        # Calculate real data values
        total_members = Member.objects.count()
        total_expenses_amount = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        total_groups = Group.objects.count()
        pending_amount = 0

        # Get additional stats for completeness
        total_expenses_count = Expense.objects.count()

        # Calculate unsettled and balanced groups for summary
        unsettled_groups = 0
        balanced_groups = 0
        for group in Group.objects.all():
            balances = calculate_balances(group)
            pending = sum(balances.values())
            if pending > 0:
                unsettled_groups += 1
                pending_amount += pending
            else:
                balanced_groups += 1

        # Get recent activities (last 15 for better visibility)
        recent_expenses = Expense.objects.select_related('group', 'added_by').order_by('-date')[:15]

        # Get system health metrics
        active_users_today = Expense.objects.filter(
            date__date=timezone.now().date()
        ).values('added_by').distinct().count()

        recent_groups = Group.objects.filter(
            created_date__date__gte=timezone.now().date() - timezone.timedelta(days=7)
        ).count()

        # Calculate growth metrics
        last_week_expenses = Expense.objects.filter(
            date__date__gte=timezone.now().date() - timezone.timedelta(days=7)
        ).aggregate(total=Sum('amount'))['total'] or 0

        extra_context = extra_context or {}
        extra_context.update({
            'total_members': total_members,
            'total_expenses': float(total_expenses_amount),
            'total_groups': total_groups,
            'total_expenses_count': total_expenses_count,
            'pending_amount': float(pending_amount),
            'balanced_groups': balanced_groups,
            'unsettled_groups': unsettled_groups,
            'recent_expenses': recent_expenses,
            'active_users_today': active_users_today,
            'recent_groups': recent_groups,
            'last_week_expenses': float(last_week_expenses),
            'current_timestamp': timezone.now().timestamp(),
        })

        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = ExpenseSplitterAdminSite(name='expense_admin')

# Register models with custom admin site
admin_site.register(Member, MemberAdmin)
admin_site.register(Expense, ExpenseAdmin)
admin_site.register(Group, GroupAdmin)
