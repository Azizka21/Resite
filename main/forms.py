from django import forms
from main.models import *

class ListSelectionForm(forms.Form):
    list = forms.ModelChoiceField(queryset=None, empty_label="Выберите список", required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['list'].queryset = List.objects.filter(user=user)

class ListEditForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name', 'people']  # Указываем, что будем работать с полями name и people