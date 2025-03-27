from rest_framework import serializers
from dcim.api.serializers import NestedDeviceSerializer
from dcim.models import Cable, PowerPort, PowerOutlet, PowerFeed

class CablePathSegmentSerializer(serializers.Serializer):
    cable = serializers.HyperlinkedRelatedField(
        view_name='dcim-api:cable-detail',
        queryset=Cable.objects.all()
    )
    a_side = serializers.SerializerMethodField()
    b_side = serializers.SerializerMethodField()
    device_a = NestedDeviceSerializer()
    device_b = NestedDeviceSerializer()

    def get_a_side(self, obj):
        return str(obj['a_side'])

    def get_b_side(self, obj):
        return str(obj['b_side'])

class TraceResultSerializer(serializers.Serializer):
    start = serializers.DictField()
    path = CablePathSegmentSerializer(many=True)
    is_complete = serializers.BooleanField()
