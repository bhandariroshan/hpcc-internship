import os
from django.contrib import admin

# Register your models here. 
from import_export.admin import  ExportMixin 
from spotprices.models import SpotPrices 
 

@admin.register(SpotPrices)
class SpotPricesAdmin(admin.ModelAdmin):
    list_display = [
        "region", "size", "time", "api_price","cli_price",
        "pay_as_you_go_price", "one_year_reserved_price", "three_year_reserved_price"
    ]
