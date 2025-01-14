from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules, Select2Widget
from wtforms.fields.choices import SelectMultipleField

from models import TypeModel

class TypeAdminView(ModelView):
    # Define the columns to be displayed in the list view
    column_list = ['id', 'label', 'code']

    # Columns that should be excluded from the list view
    column_exclude_list = ['stores']

    # Fields to include in the create/edit form
    form_columns = ['label', 'code']

    # Optionally, you can exclude columns from being displayed in the form
    form_excluded_columns = ['stores']


    # Custom labels for columns
    column_labels = {
        'id': 'ID',
        'label': 'Label',
        'code': 'Code',
        # 'stores': 'Stores'
    }

    # Searchable columns
    column_searchable_list = ['label', 'code']

    # Sortable columns
    column_sortable_list = ['id', 'label', 'code']

    # Filters for the list view
    column_filters = ['label', 'code']