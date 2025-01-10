from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules


class CategoryAdminView(ModelView):
    # Fields to display in the list view
    column_list = ['id', 'label', 'description', 'created_at', 'stores', 'sub_categories']

    # Exclude fields from the form view
    form_excluded_columns = ['stores', 'sub_categories']

    # Fields to include in the create/edit form
    form_columns = ['label', 'description']  # Only these fields should be in the form

    # Form rules (optional, just to group fields)
    form_create_rules = [
        rules.FieldSet(['label', 'description'], header='Category Details'),
    ]

    # Customize how relationships are displayed in the list view
    column_formatters = {
        'stores': lambda view, context, model, name: ', '.join([store.title for store in model.stores]),
        'sub_categories': lambda view, context, model, name: ', '.join(
            [sub_category.label for sub_category in model.sub_categories]),
    }

    # Customize the labels for the columns
    column_labels = {
        'id': 'ID',
        'label': 'Category Name',
        'description': 'Description',
        'created_at': 'Created At',
        'stores': 'Associated Stores',
        'sub_categories': 'Sub-Categories'
    }

    # Searchable fields
    column_searchable_list = ['label', 'description']

    # Sortable fields
    column_sortable_list = ['id', 'label', 'created_at']

    # Filters for the list view
    column_filters = ['created_at']

