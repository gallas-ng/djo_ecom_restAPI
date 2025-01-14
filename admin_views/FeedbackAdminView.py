import datetime

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from wtforms import SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask import request
from models import FeedbackModel, natureEnum, UserModel, ProductModel
from db import db

class FeedbackAdminView(ModelView):
    # Fields to include in the create/edit form
    form_columns = ['message', 'nature', 'user', 'product']


    # Customize the nature field in the form to use the enum choices
    def on_form_prefill(self, form, id):
        # When editing, you can prefill the form if needed
        pass

    def on_model_change(self, form, model, is_created):
        # This is where you can handle things before saving the model
        if is_created:
            model.created_at = datetime.datetime.now(datetime.UTC)  # Set timestamp on creation if needed
        return super().on_model_change(form, model, is_created)

    # Customize the form field for nature (feedback type)
    form_args = {
        'user': {
            'query_factory': lambda : UserModel.query().all(),
            'get_label': 'username',
            'allow_blank': True,
        },
        'product': {
            'query_factory': lambda: ProductModel.query.all(),  # Fetch all users
            'get_label': 'label',  # Use the username as the label for each user
            'allow_blank': True,  # Allow the field to be blank
        }
    }
    form_overrides = {
        'user': QuerySelectField,
        'product': QuerySelectField
    }

    # Display columns for list view
    column_list = ['id', 'message', 'nature', 'user', 'product', 'created_at']

    # Customize column labels
    column_labels = {
        'id': 'ID',
        'message': 'Message',
        'nature': 'Nature of Feedback',
        'user': 'User',
        'product': 'Product',
        'created_at': 'Created At'
    }

    # Searchable fields in the admin panel
    column_searchable_list = ['message', 'nature']

    # Sortable fields
    column_sortable_list = ['created_at', 'user', 'product']

    # Filters for the list view
    column_filters = ['nature', 'created_at']


