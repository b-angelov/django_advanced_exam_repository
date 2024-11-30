from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget

from izpitnik.styling.models import Setting
from izpitnik.styling.widgets.styling_widget import StylingWidget


class SettingsChangelistForm(forms.ModelForm):


    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        value_field = self.fields['value']
        value_field.widget = StylingWidget(mode=self.initial['type'])

    # def get_initial_for_field(self, field, field_name):
    #     initial = self.initial.get(field_name, field.initial)
    #     if field_name == "type" and initial.lower() == "col":
    #         print(self.fields['value'].widget)
    #         field.widget = AdminTextInputWidget(attrs={"type":"color"})
    #         print(self.fields['value'].widget)
    #     print(field_name,initial)
    #     return super().get_initial_for_field(field,field_name)
    #     return initial


    class Meta:
        model = Setting
        fields = "__all__"





