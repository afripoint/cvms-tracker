from rest_framework import serializers
from .models import Consignment, Tracker

class ConsignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignment
        fields = '__all__'  



class TrackerSerializer(serializers.ModelSerializer):
    bill_of_ladding = serializers.SlugRelatedField(
        queryset=Consignment.objects.all(), slug_field="bill_of_ladding", required=True
    )
    class Meta:
        model = Tracker
        fields = ['bill_of_ladding', 'user_id', 'tracking_id']
        read_only_fields = ['tracking_id']

    def create(self, validated_data):
        # Extract bill_of_ladding and user_id from validated data
        bill_of_ladding = validated_data.pop('bill_of_ladding')
        
        # Try to find the Consignment with the given bill_of_ladding
        try:
            consignment = Consignment.objects.get(bill_of_ladding=bill_of_ladding)
        except Consignment.DoesNotExist:
            raise serializers.ValidationError("Consignment with the given bill_of_ladding does not exist.")
        
        # Create and return the Tracker instance
        tracker = Tracker.objects.create(consignment=consignment, **validated_data)
        return tracker
        