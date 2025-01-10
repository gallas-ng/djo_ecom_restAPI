from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

class SubCategoryAdminView(ModelView):
    # Fields to display in the list view
    column_list = ['id', 'label', 'description', 'created_at', 'category', 'products']

    # Exclude fields from the form view (we don't want to edit products during creation)
    form_excluded_columns = ['products']

    # Fields to include in the create/edit form
    form_columns = ['label', 'description', 'category']  # Only these fields should be in the form

    # Form rules (optional, just to group fields)
    form_create_rules = [
        rules.FieldSet(['label', 'description', 'category'], header='Sub-Category Details'),
    ]

    # Customize how relationships are displayed in the list view
    column_formatters = {
        'category': lambda view, context, model, name: model.category.label if model.category else 'No Category',
        'products': lambda view, context, model, name: ', '.join(
            [product.title for product in model.products]) if model.products else 'No Products'
    }

    # Customize the labels for the columns
    column_labels = {
        'id': 'ID',
        'label': 'Sub-Category Name',
        'description': 'Description',
        'created_at': 'Created At',
        'category': 'Category',
        'products': 'Products'
    }

    # Searchable fields
    column_searchable_list = ['label', 'description']

    # Sortable fields
    column_sortable_list = ['id', 'label', 'created_at']

    # Filters for the list view
    column_filters = ['created_at']

    def on_model_change(self, form, model, is_created):
        # Ensure products are not added during creation
        if is_created and model.products:
            model.products.clear()  # Clear the products list if it was inadvertently set

        return super().on_model_change(form, model, is_created)
