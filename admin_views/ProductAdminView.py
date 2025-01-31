import cloudinary
import cloudinary.uploader
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from wtforms.fields.simple import FileField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from models import SubCategoryModel, StoreModel, OptionModel


class ProductAdminView(ModelView):
    # Fields to display in the list view
    column_list = ['id', 'label', 'price_vat', 'price_ht', 'quantity', 'weight', 'rating', 'ref', 'created_at', 'sub_category', 'store', 'options']

    # Exclude feedbacks field from the form view
    form_excluded_columns = ['feedbacks']

    # Fields to include in the create/edit form
    form_columns = ['label', 'price_vat', 'price_ht', 'quantity', 'description', 'weight', 'image', 'rating', 'ref', 'sub_category', 'store', 'options']

    form_args = {
        'sub_category': {
            'query_factory': lambda: SubCategoryModel.query.all(),  # Fetch all users
            'get_label': 'label',  # Use the username as the label for each user
            'allow_blank': True,  # Allow the field to be blank
        },
        'store': {
            'query_factory': lambda: StoreModel.query.all(),  # Fetch all users
            'get_label': 'title',  # Use the username as the label for each user
            'allow_blank': True,  # Allow the field to be blank
        },
        'options': {
            'query_factory': lambda: OptionModel.query.all(),  # Fetch all users
            'get_label': 'label',  # Use the username as the label for each user
            'allow_blank': True,  # Allow the field to be blank
        },
    }

    # Make multi-selection
    form_overrides = {
        'sub_category': QuerySelectField,
        'store': QuerySelectField,
        'options': QuerySelectMultipleField,
        'image' : FileField
    }

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

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            try:
                # Upload image to Cloudinary
                upload_result = cloudinary.uploader.upload(form.image.data)
                model.image = upload_result['secure_url']
            except Exception as e:
                raise ValueError(f"Image upload failed: {str(e)}")
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
