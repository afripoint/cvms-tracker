from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from rest_framework import status
import requests
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from trackers.models import Consignment, SearchHistory, Stages, Tracker
from trackers.serializers import (
    ConsignmentSerializer,
    GetTeaserSerialiser,
    TrackerSerializer,
)
from trackers.utils import call_custom_api_request


class ConsignmentAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Get all consignments on daily basis",
        operation_description="Get all consignments on daily basis",
    )
    def get(self, request):
        response = call_custom_api_request(endpoint="tracker", params=None)

        if not response or "data" not in response:
            return Response(
                {"error": "No data received from the API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        consignments = response["data"]

        # Fetch existing records based on unique identifier (e.g., bill_of_ladding)
        existing_bills = Consignment.objects.filter(
            bill_of_ladding__in=[c["bill_of_ladding"] for c in consignments]
        ).values_list("bill_of_ladding", flat=True)

        # Prepare new and update lists
        new_records = []
        update_records = []

        for consignment_data in consignments:
            if consignment_data["bill_of_ladding"] in existing_bills:
                # Update existing records (Batch Update)
                Consignment.objects.filter(
                    bill_of_ladding=consignment_data["bill_of_ladding"]
                ).update(
                    registration_officer=consignment_data["registration_officer"],
                    shipping_company=consignment_data["shipping_company"],
                    importer_phone=consignment_data["importer_phone"],
                    consignee=consignment_data["consignee"],
                    shipper=consignment_data["shipper"],
                    terminal=consignment_data["terminal"],
                    bonded_terminal=consignment_data["bonded_terminal"],
                    description_of_goods=consignment_data["description_of_goods"],
                    gross_weight=consignment_data["gross_weight"],
                    eta=consignment_data["eta"],
                    vessel_voyage=consignment_data["vessel_voyage"],
                    quantity=consignment_data["quantity"],
                    hs_code=consignment_data["hs_code"],
                    port_of_loading=consignment_data["port_of_loading"],
                    port_of_landing=consignment_data["port_of_landing"],
                )
            else:
                # Prepare new records for bulk insertion
                new_records.append(
                    Consignment(
                        bill_of_ladding=consignment_data["bill_of_ladding"],
                        registration_officer=consignment_data["registration_officer"],
                        shipping_company=consignment_data["shipping_company"],
                        importer_phone=consignment_data["importer_phone"],
                        consignee=consignment_data["consignee"],
                        shipper=consignment_data["shipper"],
                        terminal=consignment_data["terminal"],
                        bonded_terminal=consignment_data["bonded_terminal"],
                        description_of_goods=consignment_data["description_of_goods"],
                        gross_weight=consignment_data["gross_weight"],
                        eta=consignment_data["eta"],
                        vessel_voyage=consignment_data["vessel_voyage"],
                        quantity=consignment_data["quantity"],
                        hs_code=consignment_data["hs_code"],
                        port_of_loading=consignment_data["port_of_loading"],
                        port_of_landing=consignment_data["port_of_landing"],
                    )
                )

        # Bulk create new records in one operation
        if new_records:
            created_consignments = Consignment.objects.bulk_create(new_records)

            # Create Tracker, Stages, and TrackingRecord entries for each new consignment
            for consignment in created_consignments:
                # Create a new Tracker
                tracker = Tracker.objects.create(consignment=consignment)

                # Create an initial Stage entry for this Tracker
                Stages.objects.create(
                    tracker=tracker,
                    shipping_status="in transit",  # Set initial shipping status
                )

        response = {
            "message": "Consignment processed successfully",
            "new_records": len(new_records),
            "updated_records": len(consignments) - len(new_records),
        }
        return Response(data=response, status=status.HTTP_200_OK)


class GetTeaserAPIVIew(APIView):
    @swagger_auto_schema(
        operation_summary="Get the consignment teaser for an importer using the bill of ladding",
        operation_description="Get the consignment teaser for an importer using the bill of laddin",
        request_body=GetTeaserSerialiser,
    )
    def post(self, request, *args, **kwargs):
        bill_of_ladding = request.data.get("bill_of_ladding")

        if not bill_of_ladding:
            return Response(
                {"error": "bill_of_ladding parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            consignment = get_object_or_404(
                Consignment, bill_of_ladding=bill_of_ladding
            )

            serializer = ConsignmentSerializer(consignment)

            response = {
                "message": "Teaser fetch successfully",
                "bill_of_ladding": serializer.data.get("bill_of_ladding"),
                "description_of_goods": serializer.data.get("description_of_goods"),
                "vessel_voyage": serializer.data.get("vessel_voyage"),
                "quantity": serializer.data.get("quantity"),
                "hs_code": serializer.data.get("hs_code"),
                "port_of_loading": serializer.data.get("port_of_loading"),
                "port_of_landing": serializer.data.get("port_of_landing"),
            }
            return Response(response, status=status.HTTP_200_OK)

        except Consignment.DoesNotExist:
            return Response(
                {"error": "Consignment with the specified bill_of_ladding not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


# generate tracking ID
class TrackingIDCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="This endpoint creates a tracking ID for a consignment and bill of ladding",
        operation_description="Creates tracking Id for a given consignment",
        request_body=TrackerSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = TrackerSerializer(data=request.data)
        if serializer.is_valid():
            tracker = serializer.save()
            return Response(
                {
                    "message": "Tracking ID created successfully.",
                    "tracking_id": tracker.tracking_id,
                    "consignment": tracker.consignment.bill_of_ladding,
                    "user_id": tracker.user_id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
