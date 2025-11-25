def calculate_balances(group):
    member_paid = {}
    member_owed = {}

    expenses = group.expenses.all()

    for member in group.members.all():
        member_paid[member.name] = 0
        member_owed[member.name] = 0

    for expense in expenses:
        participants = expense.participants.all()
        num_participants = participants.count()

        if num_participants > 0:
            split_amount = expense.amount / num_participants

            added_by_member = None

            try:
                if hasattr(expense.added_by, 'member_profile') and expense.added_by.member_profile:
                    added_by_member = expense.added_by.member_profile
            except:
                pass

            if not added_by_member:
                added_by_member = group.members.filter(user=expense.added_by).first()

            if not added_by_member:
                username = expense.added_by.username.lower()
                for member in group.members.all():
                    if member.user and member.user.username.lower() == username:
                        added_by_member = member
                        break

            if not added_by_member and (expense.added_by.first_name or expense.added_by.last_name):
                full_name = f"{expense.added_by.first_name} {expense.added_by.last_name}".strip()
                if full_name:
                    for member in group.members.all():
                        if member.name.lower() == full_name.lower():
                            added_by_member = member
                            break

            if added_by_member and added_by_member.name in member_paid:
                member_paid[added_by_member.name] += expense.amount
            elif not added_by_member:
                username = expense.added_by.username
                for participant in participants:
                    if participant.name == username or (participant.user and participant.user.username == username):
                        if participant.name in member_paid:
                            member_paid[participant.name] += expense.amount
                        break

            for participant in participants:
                if participant.name in member_owed:
                    member_owed[participant.name] += split_amount

    balances = {}
    member_net = {}

    for member_name in member_paid.keys():
        net = member_paid[member_name] - member_owed[member_name]
        member_net[member_name] = net

    debtors = {name: -net for name, net in member_net.items() if net < 0}
    creditors = {name: net for name, net in member_net.items() if net > 0}

    for debtor_name, debt_amount in debtors.items():
        remaining_debt = debt_amount
        for creditor_name, credit_amount in sorted(creditors.items(), key=lambda x: x[1], reverse=True):
            if remaining_debt <= 0:
                break
            if credit_amount > 0:
                payment = min(remaining_debt, credit_amount)
                key = (debtor_name, creditor_name)
                balances[key] = payment
                remaining_debt -= payment
                creditors[creditor_name] -= payment

    return balances
