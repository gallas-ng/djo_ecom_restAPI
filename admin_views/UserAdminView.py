from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from models import GroupModel

class UserAdminView(ModelView):
    # Fields to display in the list view
    column_list = [
        'id', 'username', 'email', 'first_name', 'last_name',
        'phone', 'created_at', 'isActive', 'isStaff', 'isAdmin',
        'isSuperAdmin', 'isSeller', 'isBuyer'
    ]

    # Fields to exclude from the list view
    column_exclude_list = ['password']

    # Fields to include in the create/edit form
    form_columns = [
        'username', 'email', 'password', 'first_name', 'last_name',
        'phone', 'isActive', 'isStaff', 'isAdmin', 'isSuperAdmin',
        'isSeller', 'isBuyer', 'groups'
    ]

    # Exclude fields from the create/edit form
    form_excluded_columns = ['created_at', 'feedbacks']

    # Add a password field that hides input
    form_args = {
        'password': {
            'render_kw': {
                'type': 'password'
            }
        },
        'groups': {
            'query_factory': lambda: GroupModel.query.all(),
            'allow_blank': True,  # Allow the field to be left blank
            'get_label': 'name'  # Display the group name in the dropdown
        }
    }

    # Customize how relationships are displayed
    column_display_pk = True  # Display the primary key in the list view

    # Formatting date fields
    column_formatters = {
        'created_at': lambda view, context, model, name: model.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Read-only fields in forms (e.g., fields that should not be edited)
    form_readonly_columns = ['created_at']

    # Add some help text or group fields
    form_create_rules = [
        rules.FieldSet([  # Group related fields
            'username', 'email', 'password', 'first_name', 'last_name',
            'phone', 'isActive', 'isStaff', 'isAdmin', 'isSuperAdmin',
            'isSeller', 'isBuyer', 'groups'
        ], header='User Details'),
    ]

    # Searchable fields
    column_searchable_list = ['username', 'email', 'first_name', 'last_name']

    # Sortable fields
    column_sortable_list = ['id', 'username', 'email', 'created_at']

    # Filters for the list view
    column_filters = ['isActive', 'isAdmin', 'isSeller', 'created_at']

    # Customize labels for the columns
    column_labels = {
        'id': 'ID',
        'username': 'Username',
        'email': 'Email',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'phone': 'Phone',
        'isActive': 'Active',
        'isStaff': 'Staff',
        'isAdmin': 'Admin',
        'isSuperAdmin': 'Super Admin',
        'isSeller': 'Seller',
        'isBuyer': 'Buyer',
        'created_at': 'Created At',
        'groups': 'Groups'  # Label for the groups field
    }
