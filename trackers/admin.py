from django.contrib import admin

from trackers.models import Consignment, Stages, Tracker, TrackingRecord


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

    list_display_links = ("bill_of_ladding",)


@admin.register(Tracker)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "consignment",
        "tracking_id",
        "slug",
        "user_id",
    )

    list_display_links = ("tracking_id",)


@admin.register(Stages)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "tracker",
        "shipping_status",
        "created_at",
        "updated",
    )

    list_display_links = ("tracker",)


@admin.register(TrackingRecord)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "created_by",
        "updated_by",
        "tracking_status",
    )

    list_display_links = ("created_by",)
