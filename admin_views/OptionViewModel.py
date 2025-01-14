from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

from models import OptionModel

class OptionAdminView(ModelView):
    # Fields to include in the create/edit form
    form_columns = ['label', 'value']

    # Exclude the 'products' relationship field from the form as it will be set later
    form_excluded_columns = ['products']


    # Customize the labels for the columns in the list view
    column_labels = {
        'id': 'ID',
        'label': 'Option Label',
        'value': 'Value'
    }

    # Searchable fields in the admin panel
    column_searchable_list = ['label', 'value']

    # Sortable fields
    column_sortable_list = ['id', 'label', 'value']

    # Filters for the list view
    column_filters = ['label', 'value']

    # Add some field rules for the create/edit form
    form_create_rules = [
        rules.FieldSet(['label', 'value'], header='Option Details'),
    ]
