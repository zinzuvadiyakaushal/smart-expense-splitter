def calculate_balances(group):
    # Function to calculate balances for a group (equal split)
    balances = {}  # Dict to store who owes whom
    expenses = group.expenses.all()  # Get all expenses in the group

    for expense in expenses:
        # For each expense
        participants = expense.participants.all()  # Get participants
        num_participants = participants.count()  # Number of participants
        if num_participants > 0:
            split_amount = expense.amount / num_participants  # Equal split amount
            for participant in participants:
                # For each participant
                if participant != expense.added_by.member_profile:
                    # If not the one who added, they owe
                    key = (participant.name, expense.added_by.member_profile.name)
                    if key not in balances:
                        balances[key] = 0
                    balances[key] += split_amount  # Add to balance

    return balances  # Return the balances dict
