from db_mutations import User, Group, Expense

# Example usage:
if __name__ == "__main__":
    # Testing user creation
    User.create_user('user1', 'user1@example.com')
    User.create_user('user2', 'user2@example.com')
    User.create_user('user3', 'user3@example.com')

    all_users = User.get_all_users()
    print("All Users:")
    for user in all_users:
        print(user)

    # Testing group creation
    Group.create_group('Group A')
    Group.create_group('Group B')

    all_groups = Group.get_all_groups()
    print("\nAll Groups:")
    for group in all_groups:
        print(group)

    # Adding users to groups
    Group.add_user_to_group('user1', 'Group A')
    Group.add_user_to_group('user2', 'Group A')
    Group.add_user_to_group('user2', 'Group B')
    Group.add_user_to_group('user3', 'Group B')

    # Testing group expense creation
    Expense.create_group_expense(200, 'Group Expense', 'Group A', 'user1')
    Expense.create_group_expense(150, 'Another Group Expense', 'Group B', 'user2')

    # Testing individual expense creation
    Expense.create_individual_expense(100, 'Individual Expense for user3', 'user3', 'user3')

    all_expenses = Expense.get_all_expenses()
    print("\nAll Expenses:")
    for expense in all_expenses:
        print(expense)
