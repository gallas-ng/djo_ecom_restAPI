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

    # Exclude user and product relationships from the list view to prevent editing here
    column_exclude_list = ['user', 'product']

    # Customize the nature field in the form to use the enum choices
    def on_form_prefill(self, form, id):
        # When editing, you can prefill the form if needed
        feedback = FeedbackModel.query.get(id)
        if feedback:
            form.nature.data = feedback.nature

    def on_model_change(self, form, model, is_created):
        # This is where you can handle things before saving the model
        if is_created:
            model.created_at = datetime.datetime.now(datetime.UTC)  # Set timestamp on creation if needed
        return super().on_model_change(form, model, is_created)

    # Customize the form field for nature (feedback type)
    form_widget_args = {
        'nature': {
            'widget': SelectField(
                'Nature of Feedback',
                choices=[(tag, tag.value) for tag in natureEnum]
            )
        },
        'user': {
            'widget': QuerySelectField(
                'User',
                query_factory=lambda: db.session.query(UserModel).all(),
                get_label='username',
                allow_blank=True  # Optional, can choose to allow None for User selection
            )
        },
        'product': {
            'widget': QuerySelectField(
                'Product',
                query_factory=lambda: db.session.query(ProductModel).all(),
                get_label='label',
                allow_blank=True  # Optional, can choose to allow None for Product selection
            )
        }
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


