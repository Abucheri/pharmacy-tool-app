from django.contrib import admin
from .models import *
from .forms import *

class StockCreateAdmin(admin.ModelAdmin):
    form = StockCreateForm
    list_display = ['category', 'item_name', 'quantity']
    list_filter = ['category']
    search_fields = ['category', 'item_name']
    list_editable = ['item_name', 'quantity']


# Register your models here.
admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
