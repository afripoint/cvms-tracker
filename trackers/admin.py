from django.contrib import admin

from trackers.models import Consignment


@admin.register(Consignment)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "bill_of_ladding",
        "importer_phone",
        "registration_officer",
        "shipping_company",
        "consignee",
        "shipper",
        "terminal",
    )

    list_display_links = (
        "bill_of_ladding",
    )
