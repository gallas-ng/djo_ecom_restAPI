from flask_admin.contrib.sqla import ModelView
from wtforms.fields.choices import SelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from models import UserModel


class GroupAdminView(ModelView):
    # Displayed columns
    column_list = ['id', 'name', 'permissions', 'created_at', 'users']

    # Form fields
    form_columns = ['name', 'permissions', 'users']

    # Configure the `users` field to allow multi-selection
    form_args = {
        'users': {
            'query_factory': lambda: UserModel.query.all(),  # Fetch all users
            'get_label': 'username',  # Use the username as the label for each user
            'allow_blank': True,  # Allow the field to be blank
        }
    }

    # Make multi-selection
    form_overrides = {
        'users': QuerySelectMultipleField  # Ensure multi-selection works
    }

    # Format the `created_at` column for display
    column_formatters = {
        'created_at': lambda view, context, model, name: model.created_at.strftime('%Y-%m-%d %H:%M:%S') if model.created_at else ''
    }

    # Read-only fields in the form
    form_readonly_columns = ['created_at']

    # Sortable fields
    column_sortable_list = ['id', 'name', 'created_at']

    # Filters for the list view
    column_filters = ['name', 'created_at']

    # Searchable fields
    column_searchable_list = ['name']

    # Labels for columns
    column_labels = {
        'id': 'ID',
        'name': 'Group Name',
        'permissions': 'Permissions',
        'created_at': 'Created At',
        'users': 'Assigned Users'
    }
