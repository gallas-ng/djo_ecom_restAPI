from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

class ProductAdminView(ModelView):
    # Fields to display in the list view
    column_list = ['id', 'label', 'price_vat', 'price_ht', 'quantity', 'weight', 'rating', 'ref', 'created_at', 'sub_category', 'store', 'options']

    # Exclude feedbacks field from the form view
    form_excluded_columns = ['feedbacks']

    # Fields to include in the create/edit form
    form_columns = ['label', 'price_vat', 'price_ht', 'quantity', 'description', 'weight', 'image', 'rating', 'ref', 'sub_category', 'store', 'options']

    # Add form rules (optional)
    form_create_rules = [
        rules.FieldSet(['label', 'price_vat', 'price_ht', 'quantity', 'description', 'weight', 'image', 'rating', 'ref'], header='Product Details'),
        rules.FieldSet(['sub_category', 'store', 'options'], header='Product Relationships')
    ]

    # Customize the labels for the columns in the list view
    column_labels = {
        'id': 'ID',
        'label': 'Product Name',
        'price_vat': 'Price (VAT)',
        'price_ht': 'Price (HT)',
        'quantity': 'Quantity',
        'description': 'Description',
        'weight': 'Weight',
        'image': 'Image',
        'rating': 'Rating',
        'ref': 'Reference',
        'created_at': 'Created At',
        'sub_category': 'Sub-Category',
        'store': 'Store',
        'options': 'Options'
    }

    # Searchable fields
    column_searchable_list = ['label', 'description', 'ref']

    # Sortable fields
    column_sortable_list = ['id', 'label', 'created_at', 'price_vat', 'price_ht']

    # Filters for the list view
    column_filters = ['created_at', 'price_vat', 'price_ht', 'quantity', 'rating']

    # Customize how relationships are displayed in the list view
    column_formatters = {
        'sub_category': lambda view, context, model, name: model.sub_category.label if model.sub_category else 'No Sub-Category',
        'store': lambda view, context, model, name: model.store.title if model.store else 'No Store',
        'options': lambda view, context, model, name: ', '.join([option.label for option in model.options]) if model.options else 'No Options'
    }

    def on_model_change(self, form, model, is_created):
        # Ensure no feedbacks are linked when creating or editing a product
        if is_created and model.feedbacks:
            model.feedbacks.clear()  # Clear the feedbacks field if it was inadvertently set

        return super().on_model_change(form, model, is_created)
