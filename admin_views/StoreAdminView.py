from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin.form.widgets import Select2Widget
from models import TypeModel, UserModel, CategoryModel, AddressModel
from db import db
from resources.category import Category


class StoreAdminView(ModelView):
    # Fields to display in the list view
    column_list = ['id', 'title', 'phone', 'address', 'types', 'owner', 'categories', 'products']

    # Fields to exclude from the list view
    column_exclude_list = ['address', 'types', 'categories', 'products']

    # Fields to include in the create/edit form
    form_columns = ['title', 'phone', 'address', 'types', 'owner', 'categories']

    # Exclude fields from the create/edit form
    form_excluded_columns = ['created_at']

    # Form arguments to specify which fields should be used in forms
    form_args = {

        'address': {
            'query_factory': lambda: AddressModel.query.all(), 'get_label': 'street', 'allow_blank': True,
            # 'widget': Select2Widget(multiple=True)  # Allows multiple types selection
        },

        'types': {
            'query_factory': lambda: TypeModel.query.all(), 'get_label': 'label', 'allow_blank': True,
            # 'widget': Select2Widget(multiple=True)  # Allows multiple types selection
        },
        'owner': {
            'query_factory': lambda: UserModel.query.all(),  # Fetch all users
            'get_label': 'username',  # Use the username as the label for each user
            'allow_blank': True,
        },
        'categories': {
            'query_factory': lambda: CategoryModel.query.all(), 'get_label': 'label', 'allow_blank': True,
            # 'widget': Select2Widget(multiple=True)  # Categories selection widget
        },

    }

    form_overrides = {
        'categories': QuerySelectMultipleField,
        'types': QuerySelectMultipleField# Ensure multi-selection works
    }
    # Form rules to group fields in FieldSets
    form_create_rules = [
        rules.FieldSet([
            'title', 'phone', 'address', 'types', 'owner', 'categories'
        ], header='Store Details')
    ]

    # Customize the labels for the columns
    column_labels = {
        'id': 'ID',
        'title': 'Store Title',
        'phone': 'Phone Number',
        'types': 'Store Types',
        'owner': 'Store Owner',
        'categories': 'Categories',
    }

    # Making the address, types, and owner mandatory in the form
    def validate(self, form):
        if not form.types.data:
            form.types.errors.append('At least one type is required.')
            return False
        if not form.owner.data:
            form.owner.errors.append('Owner is required.')
            return False
        return True

    # Handle the creation and validation of the store
    def on_model_change(self, form, model, is_created):
        if is_created:
            # Ensure that at least one type and the owner are provided
            if not model.types:
                raise ValueError('At least one type is required.')
            if not model.owner:
                raise ValueError('Owner is mandatory.')

        return super().on_model_change(form, model, is_created)

    # # Customize the `types` and `owner` selection
    # form_widget_args = {
    #     'types': {
    #         'widget': QuerySelectField(
    #             'Types',
    #             query_factory=lambda: db.session.query(TypeModel).all(),
    #             get_label='label',  # Displaying the `label` from `TypeModel`
    #             allow_blank=True,  # Allow blank selection (types are optional)
    #             widget=Select2Widget(multiple=True)  # Multiple selection enabled
    #         )
    #     },
    #     'owner': {
    #         'widget': QuerySelectField(
    #             'Owner',
    #             query_factory=lambda: db.session.query(UserModel).all(),
    #             get_label='username',  # Displaying the `username` from `UserModel`
    #             allow_blank=True  # Allow blank selection (owner is optional)
    #         )
    #     }
    # }

