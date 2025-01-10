from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules, Select2Widget
from wtforms.fields.choices import SelectMultipleField

from models import TypeModel

class TypeAdminView(ModelView):
    # Define the columns to be displayed in the list view
    column_list = ['id', 'label', 'code',
                   # 'stores'
                   ]

    # Columns that should be excluded from the list view
    column_exclude_list = ['stores']

    # Fields to include in the create/edit form
    form_columns = ['label', 'code',
                    # 'stores'
                    ]

    # Optionally, you can exclude columns from being displayed in the form
    form_excluded_columns = []

    # Allow users to select multiple stores (but it's optional)
    form_widget_args = {
        'stores': {
            'widget': Select2Widget(multiple=True)
        }
    }

    # Display the relationship fields as multiple choice options (Select2Widget is used for better UI)
    form_overrides = {
        'stores': SelectMultipleField  # Using SelectMultipleField for stores
    }

    form_args = {
        'stores': {
            'validators': []  # We don't need validation here, since stores can be optional
        }
    }

    def on_model_change(self, form, model, is_created):
        # Perform any additional actions when a new type is created or edited
        # If you want to add extra validations, you can do that here
        return super().on_model_change(form, model, is_created)

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