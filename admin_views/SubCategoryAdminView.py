from flask_admin.contrib.sqla import ModelView

from flask_admin.form import rules
from wtforms_sqlalchemy.fields import QuerySelectField

from models import CategoryModel


class SubCategoryAdminView(ModelView):
    # Fields to display in the list view
    column_list = ['id', 'label', 'description', 'created_at', 'category']

    # Exclude fields from the form view (we don't want to edit products during creation)
    form_excluded_columns = ['products']

    # Fields to include in the create/edit form
    form_columns = ['label', 'description', 'category']  # Only these fields should be in the form

    form_args = {
        'category': {
            'query_factory': lambda: CategoryModel.query.all(),  # Fetch all users
            'get_label': 'label',  # Use the username as the label for each user
            'allow_blank': True,  # Allow the field to be blank
        }
    }

    # Make multi-selection
    form_overrides = {
        'category': QuerySelectField  # Ensure multi-selection works
    }

    # Form rules (optional, just to group fields)
    form_create_rules = [
        rules.FieldSet(['label', 'description', 'category'], header='Sub-Category Details'),
    ]

    # Customize how relationships are displayed in the list view
    column_formatters = {
        'category': lambda view, context, model, name: model.category.label if model.category else 'No Category',
        # 'products': lambda view, context, model, name: ', '.join(
        #     [product.title for product in model.products]) if model.products else 'No Products'
    }

    # Customize the labels for the columns
    column_labels = {
        'id': 'ID',
        'label': 'Sub-Category Name',
        'description': 'Description',
        'created_at': 'Created At',
        'category': 'Category',
    }

    # Searchable fields
    column_searchable_list = ['label', 'description']

    # Sortable fields
    column_sortable_list = ['id', 'label', 'created_at']

    # Filters for the list view
    column_filters = ['created_at']

