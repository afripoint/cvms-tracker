from django.db import models
from django.db import transaction
import uuid
from django.utils.text import slugify

# from accounts_mobile.send import send_message


class Consignment(models.Model):
    bill_of_ladding = models.CharField(
        max_length=150, unique=True, blank=True, null=True
    )
    registration_officer = models.CharField(max_length=150, blank=True, null=True)
    shipping_company = models.CharField(max_length=150, blank=True, null=True)
    importer_phone = models.CharField(max_length=50, blank=True, null=True)
    consignee = models.CharField(max_length=150, blank=True, null=True)
    shipper = models.CharField(max_length=150, blank=True, null=True)
    terminal = models.CharField(max_length=150, blank=True, null=True)
    bonded_terminal = models.CharField(max_length=150, blank=True, null=True)
    description_of_goods = models.TextField(blank=True, null=True)
    gross_weight = models.CharField(max_length=50, blank=True, null=True)
    eta = models.DateField(blank=True, null=True)
    vessel_voyage = models.CharField(max_length=150, blank=True, null=True)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=250, blank=True, null=True)
    charges = models.CharField(max_length=50, blank=True, null=True)
    container_id = models.CharField(max_length=50, blank=True, null=True)
    hs_code = models.CharField(max_length=250, blank=True, null=True)
    port_of_loading = models.CharField(max_length=150, blank=True, null=True)
    port_of_landing = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"consignment"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.bill_of_ladding) + str(uuid.uuid4())

        super().save(*args, **kwargs)


# To generate the Tracking ID
class Tracker(models.Model):
    consignment = models.ForeignKey(
        Consignment, related_name="tracker", on_delete=models.CASCADE
    )
    tracking_id = models.CharField(max_length=150, unique=True, blank=True, null=True)
    slug = models.CharField(max_length=250, unique=True, blank=True, null=True)
    user_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.tracking_id} for {self.consignment.consignee}"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.consignment.bill_of_ladding) + str(uuid.uuid4())

        if not self.tracking_id:
            prefix = "CUST"
            unique_id = uuid.uuid4().hex[:6].upper()
            self.tracking_id = f"{prefix}-{unique_id}"

        super().save(*args, **kwargs)

       

class Stages(models.Model):
    SHIPMENT_STATUS = (
        ("in terminal", "In Terminal"),
        ("in warehouse", "In Warehouse"),
        ("undergoing inspection", "Undergoing Inspection"),
        ("payment", "Payment"),
        ("cleared", "Cleared"),
        ("in transit", "In Transit"),
    )
    tracker = models.ForeignKey(
        Tracker, related_name="stages", on_delete=models.CASCADE
    )
    shipping_status = models.CharField(
        max_length=50, choices=SHIPMENT_STATUS, default="in transit"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment status of the {self.tracker.consignment.consignee} with {self.tracker.tracking_id}"


class TrackingRecord(models.Model):
    TRACKING_STATUS = (
        ("tracking created", "Tracking Created"),
        ("tracking updated", "Tracking Updated"),
    )
    created_by = models.ForeignKey(
        Consignment, related_name="consignment", on_delete=models.CASCADE
    )
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    tracking_status = models.CharField(
        max_length=50, choices=TRACKING_STATUS, default="tracking created"
    )
    slug = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.created_by.consignee

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.created_by.bill_of_ladding) + str(uuid.uuid4())

        super().save(*args, **kwargs)


class SearchHistory(models.Model):
    consignment = models.ForeignKey(Consignment, on_delete=models.CASCADE)
    stages = models.ForeignKey(Stages, on_delete=models.CASCADE)
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE)
    slug = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"search history for {self.consignment.bill_of_ladding}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.consignment.bill_of_ladding) + str(uuid.uuid4())
        super().save(*args, **kwargs)
