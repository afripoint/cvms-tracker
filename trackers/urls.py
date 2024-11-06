from django.urls import path

from trackers.views import ConsignmentAPIView, GetTeaserAPIVIew, TrackingIDCreateAPIView

urlpatterns = [
    path("get-teaser/", GetTeaserAPIVIew.as_view(), name='get-teaser'),
    path("get-consignment/", ConsignmentAPIView.as_view(), name='get-consignment'),
    path("generate_tracking_id/", TrackingIDCreateAPIView.as_view(), name='generate-tracking-id'),
]
