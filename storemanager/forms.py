from django import forms
from django.contrib.admin import widgets
from .models import *
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        # fields = ['category', 'item_name', 'quantity', 'date']
        fields = ['category', 'item_name', 'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This is a required field!!')
        # for instance in Stock.objects.all():
        #     if instance.category == category:
        #         raise forms.ValidationError(category + ' already exists...')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This is a required field!!')
        for instance in Stock.objects.all():
            if instance.item_name == item_name:
                raise forms.ValidationError(str(item_name) + ' already exists!!')
        return item_name


class DrugsHistorySearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    # start_date = forms.DateTimeField(required=False)
    # start_date = forms.DateTimeField(required=False,
    #                                  input_formats=['%Y-%m-%d'],
    #                                  widget=DatePickerInput(format='%Y-%m-%d'))
    start_date = forms.DateField(required=False, widget=DatePickerInput(format='%Y-%m-%d'))
    # end_date = forms.DateTimeField(required=False,
    #                                input_formats=['%Y-%m-%d'],
    #                                widget=DatePickerInput(format='%Y-%m-%d'))
    end_date = forms.DateField(required=False, widget=DatePickerInput(format='%Y-%m-%d'))

    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'start_date', 'end_date']


class DrugsSearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        # fields = ['category', 'item_name']
        fields = ['item_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This is a required field!!')
        # for instance in Stock.objects.all():
        #     if instance.category == category:
        #         raise forms.ValidationError(category + ' already exists...')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This is a required field!!')
        return item_name


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issued_quantity', 'issued_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        # fields = ['received_quantity', 'received_by']
        fields = ['received_quantity']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
