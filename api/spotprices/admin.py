import os
from django.contrib import admin

# Register your models here. 
from import_export import resources
from import_export.admin import  ExportMixin 
from spotprices.models import SpotPrices, EvictionNotices
 

class SpotPricesResource(resources.ModelResource):
    class Meta:
        fields = [
            "region", "size", "time", "api_price","cli_price",
            "pay_as_you_go_price", "one_year_reserved_price", "three_year_reserved_price"
        ]

        export_order = [
            "region", "size", "time", "api_price","cli_price",
            "pay_as_you_go_price", "one_year_reserved_price", "three_year_reserved_price"
        ]

        import_order = [
            "region", "size", "time", "api_price","cli_price",
            "pay_as_you_go_price", "one_year_reserved_price", "three_year_reserved_price"
        ]

        model = SpotPrices


@admin.register(SpotPrices)
class SpotPricesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        "region", "size", "time", "api_price","cli_price",
        "pay_as_you_go_price", "one_year_reserved_price", "three_year_reserved_price"
    ]
    search_fields = ('region', 'size', )
    resource_class = SpotPricesResource


class EvictionNoticesResource(resources.ModelResource):
    class Meta:
        fields = [
            "start_time",
            "ip_address",
            "vm_name",
            "vm_region",
            "cluster_name",
            "cluster_region",
            "eviction_time",
            "eviction_notice"
        ]

        export_order = [
            "start_time",
            "ip_address",
            "vm_name",
            "vm_region",
            "cluster_name",
            "cluster_region",
            "eviction_time",
            "eviction_notice"
        ]

        import_order = [
            "start_time",
            "ip_address",
            "vm_name",
            "vm_region",
            "cluster_name",
            "cluster_region",
            "eviction_time",
            "eviction_notice"
        ]

        model = EvictionNotices


@admin.register(EvictionNotices)
class EvictionNoticesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        "start_time",
        "ip_address",
        "vm_name",
        "vm_region",
        "cluster_name",
        "cluster_region",
        "eviction_time",
        "eviction_notice"
    ]
    search_fields = ('vm_name',)
    resource_class = EvictionNoticesResource