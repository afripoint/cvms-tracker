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
from trackers.serializers import ConsignmentSerializer, TrackerSerializer
from trackers.utils import call_custom_api_request


# wrong implementation: just add query param to the endpoint and use it just liek Damilare's endpoint for verification
class GetTeaserAPIVIew(APIView):
    def post(self, request, *args, **kwargs):
        bill_of_ladding = request.data.get("bill_of_ladding")

        if not bill_of_ladding:
            return Response(
                {"error": "bill_of_ladding parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            consignment = get_object_or_404(Consignment, bill_of_ladding=bill_of_ladding)
            tracker = get_object_or_404(Tracker, consignment=consignment)
            stages = get_object_or_404(Stages, tracker=tracker)

            serializer = ConsignmentSerializer(consignment)

            SearchHistory.objects.create(
                consignment=consignment,
                stages=stages,
                tracker=tracker,
            )

            response = {
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


# view tracking/search history
