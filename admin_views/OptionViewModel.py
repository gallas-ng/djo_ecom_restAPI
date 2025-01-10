from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

from models import OptionModel

class OptionAdminView(ModelView):
    # Fields to include in the create/edit form
    form_columns = ['label', 'description', 'type', 'typeArray']

    # Exclude the 'products' relationship field from the form as it will be set later
    form_excluded_columns = ['products']

    # Customize the form to handle dynamic population of the typeArray based on the selected type
    def on_form_prefill(self, form, id):
        option = OptionModel.query.get(id)
        if option and option.type == 'color':
            form.typeArray.choices = [('black', 'black'), ('white', 'white')]
        elif option and option.type == 'size':
            form.typeArray.choices = [('large', 'large'), ('small', 'small')]

    # Customize the form to handle dynamic population of the typeArray before saving the model
    def on_model_change(self, form, model, is_created):
        if model.type == 'color':
            model.typeArray = 'black'  # Set default value if necessary, or adjust as needed
        elif model.type == 'size':
            model.typeArray = 'large'  # Set default value if necessary, or adjust as needed

        return super().on_model_change(form, model, is_created)

    # Customize the labels for the columns in the list view
    column_labels = {
        'id': 'ID',
        'label': 'Option Label',
        'description': 'Description',
        'type': 'Type',
        'typeArray': 'Values'
    }

    # Searchable fields in the admin panel
    column_searchable_list = ['label', 'description', 'type']

    # Sortable fields
    column_sortable_list = ['id', 'label', 'type']

    # Filters for the list view
    column_filters = ['type', 'typeArray']

    # Add some field rules for the create/edit form
    form_create_rules = [
        rules.FieldSet(['label', 'description'], header='Option Details'),
        rules.FieldSet(['type', 'typeArray'], header='Option Type and Values')
    ]
