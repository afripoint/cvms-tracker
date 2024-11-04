from django.urls import path

from trackers.views import GetTeaserAPIVIew, TrackingIDCreateAPIView

urlpatterns = [
    path("", GetTeaserAPIVIew.as_view(), name='get-teaser'),
    path("generate_tracking_id/", TrackingIDCreateAPIView.as_view(), name='generate-tracking-id')
]
