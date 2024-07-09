from datetime import datetime
from schema import atlas_client, AtlasClient

class User:
    @staticmethod
    def create_user(username, email):
        user = {
            'username': username,
            'email': email,
            'expenses': []
        }
        return atlas_client.get_collection('users').insert_one(user)

    @staticmethod
    def get_user_by_username(user_username):
        return atlas_client.get_collection('users').find_one({'username': user_username})

    @staticmethod
    def get_all_users():
        return atlas_client.get_collection('users').find()

class Group:
    @staticmethod
    def create_group(name):
        group = {
            'name': name,
            'members': []
        }
        return atlas_client.get_collection('groups').insert_one(group)

    @staticmethod
    def get_group_by_name(group_name):
        return atlas_client.get_collection('groups').find_one({'name': group_name})

    @staticmethod
    def add_user_to_group(user_username, group_name):
        group = Group.get_group_by_name(group_name)
        if group:
            members = group.get('members', [])
            if user_username not in members:
                members.append(user_username)
            atlas_client.get_collection('groups').update_one(
                {'name': group_name},
                {'$set': {'members': members}}
            )

    @staticmethod
    def get_all_groups():
        return atlas_client.get_collection('groups').find()

class Expense:
    @staticmethod
    def create_group_expense(amount, description, group_name, logged_in_user_id):
        group = Group.get_group_by_name(group_name)
        if not group:
            raise Exception(f"Group with name '{group_name}' not found.")

        # Retrieve group members
        group_members = group.get('members', [])

        # Calculate share per member
        num_members = len(group_members)
        share_per_member = amount / num_members

        # Create expense for the group
        expense = {
            'amount': amount,
            'description': description,
            'group_name': group_name,
            'created_at': datetime.utcnow(),
            'shared_with': [],
            'created_by': logged_in_user_id  # Assuming the logged-in user creates the expense
        }

        for member in group_members:
            expense['shared_with'].append({
                'username': member,
                'share': share_per_member
            })

        return atlas_client.get_collection('expenses').insert_one(expense)

    @staticmethod
    def create_individual_expense(amount, description, user_username, logged_in_user_id):
        user = User.get_user_by_username(user_username)
        if not user:
            raise Exception(f"User with username '{user_username}' not found.")

        # Create expense for the user
        expense = {
            'amount': amount,
            'description': description,
            'username': user_username,
            'created_at': datetime.utcnow(),
            'shared_with': [{
                'username': user_username,
                'share': amount  # Full amount is shared with the user in individual expenses
            }],
            'created_by': logged_in_user_id  # Assuming the logged-in user creates the expense
        }
        return atlas_client.get_collection('expenses').insert_one(expense)

    @staticmethod
    def get_all_expenses():
        return atlas_client.get_collection('expenses').find()
