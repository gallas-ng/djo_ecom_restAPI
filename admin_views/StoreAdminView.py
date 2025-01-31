import cloudinary
import cloudinary.uploader
from wtforms.fields.choices import SelectMultipleField, SelectField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import StringField, FileField
from wtforms.form import Form
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin.form.widgets import Select2Widget
from models import TypeModel, UserModel, CategoryModel, AddressModel, StoreModel
from db import db
from resources.category import Category

class StoreForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    phone = StringField('Phone')
    image = FileField('Image')
    street = StringField('Street', validators=[DataRequired()])
    number = StringField('Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    longitude = FloatField('Longitude')
    latitude = FloatField('Latitude')
    types = QuerySelectMultipleField(
        'Types',
        query_factory=lambda: TypeModel.query.all(),
        get_label='label',
        allow_blank=True
    )
    categories = QuerySelectMultipleField('Categories', query_factory=lambda: CategoryModel.query.all(),get_label='label', allow_blank=True)
    owner = QuerySelectField('Owner', query_factory=lambda: UserModel.query.all(), get_label='username', allow_blank=True)

class StoreAdminView(ModelView):
    form = StoreForm
    form_excluded_columns = ['products']

    def on_form_prefill(self, form, id):
        store = StoreModel.query.get(id)
        if store:
            form.types.data = store.types
            form.categories.data = store.categories
            form.owner.data = store.owner

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            try:
                # Upload image to Cloudinary
                upload_result = cloudinary.uploader.upload(form.image.data)
                model.image = upload_result['secure_url']
            except Exception as e:
                raise ValueError(f"Image upload failed: {str(e)}")

        if is_created:
            address = AddressModel(
                street=form.street.data,
                number=form.number.data,
                city=form.city.data,
                state=form.state.data,
                longitude=form.longitude.data,
                latitude=form.latitude.data
            )
            model.address = address
            # db.session.add(address)
        else:
            model.address.street = form.street.data
            model.address.number = form.number.data
            model.address.city = form.city.data
            model.address.state = form.state.data
            model.address.longitude = form.longitude.data
            model.address.latitude = form.latitude.data

        model.types = TypeModel.query.filter(TypeModel.id.in_([t.id for t in form.types.data])).all()
        model.categories = CategoryModel.query.filter(CategoryModel.id.in_([c.id for c in form.categories.data])).all()
        model.owner_id = form.owner.data.id


#
# class StoreAdminView(ModelView):
#     # Fields to display in the list view
#     column_list = ['id', 'title', 'phone', 'address', 'types', 'owner', 'categories', 'products']
#
#     # Fields to exclude from the list view
#     column_exclude_list = ['address', 'types', 'categories', 'products']
#
#     # Fields to include in the create/edit form
#     form_columns = ['title', 'phone', 'address', 'types', 'owner', 'categories']
#
#
#     # Exclude fields from the create/edit form
#     form_excluded_columns = ['created_at']
#
#     # Form arguments to specify which fields should be used in forms
#     form_args = {
#
#         'address': {
#             'query_factory': lambda: AddressModel.query.all(), 'get_label': 'street', 'allow_blank': True,
#             'widget': Select2Widget(multiple=False)  # Allows multiple types selection
#         },
#
#         'types': {
#             'query_factory': lambda: TypeModel.query.all(), 'get_label': 'label', 'allow_blank': True,
#             'widget': Select2Widget(multiple=True)  # Allows multiple types selection
#         },
#         'owner': {
#             'query_factory': lambda: UserModel.query.all(),  # Fetch all users
#             'get_label': 'username',  # Use the username as the label for each user
#             'allow_blank': True,
#             'widget': Select2Widget(multiple=False)
#         },
#         'categories': {
#             'query_factory': lambda: CategoryModel.query.all(), 'get_label': 'label', 'allow_blank': True,
#             'widget': Select2Widget(multiple=True)  # Categories selection widget
#         },
#
#     }
#
#     # form_overrides = {
#     #     'categories': QuerySelectMultipleField,
#     #     'types': QuerySelectMultipleField# Ensure multi-selection works
#     # }
#     # Form rules to group fields in FieldSets
#     form_create_rules = [
#         rules.FieldSet([
#             'title', 'phone', 'address', 'types', 'owner', 'categories'
#         ], header='Store Details')
#     ]
#
#     # Customize the labels for the columns
#     column_labels = {
#         'id': 'ID',
#         'title': 'Store Title',
#         'phone': 'Phone Number',
#         'types': 'Store Types',
#         'owner': 'Store Owner',
#         'categories': 'Categories',
#     }

    # # Making the address, types, and owner mandatory in the form
    # def validate(self, form):
    #     if not form.types.data:
    #         form.types.errors.append('At least one type is required.')
    #         return False
    #     if not form.owner.data:
    #         form.owner.errors.append('Owner is required.')
    #         return False
    #     return True
    #
    # # Handle the creation and validation of the store
    # def on_model_change(self, form, model, is_created):
    #     if is_created:
    #         # Ensure that at least one type and the owner are provided
    #         if not model.types:
    #             raise ValueError('At least one type is required.')
    #         if not model.owner:
    #             raise ValueError('Owner is mandatory.')
    #
    #     return super().on_model_change(form, model, is_created)

