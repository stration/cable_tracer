from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import CablePath, PathSegment
from dcim.api.serializers import NestedDeviceSerializer, NestedPowerPortSerializer
from dcim.models import Cable

class PathSegmentSerializer(NetBoxModelSerializer):
    cable = serializers.HyperlinkedIdentityField(
        view_name='dcim-api:cable-detail'
    )
    device_a = NestedDeviceSerializer()
    port_a = NestedPowerPortSerializer()
    device_b = NestedDeviceSerializer()
    port_b = NestedPowerPortSerializer()

    class Meta:
        model = PathSegment
        fields = [
            'id', 'cable', 'sequence', 
            'device_a', 'port_a', 
            'device_b', 'port_b',
            'display'
        ]

class CablePathSerializer(NetBoxModelSerializer):
    start_device = NestedDeviceSerializer()
    start_port = NestedPowerPortSerializer()
    end_device = NestedDeviceSerializer()
    end_port = NestedPowerPortSerializer()
    segments = PathSegmentSerializer(many=True, read_only=True)
    path_length = serializers.IntegerField(read_only=True)
    is_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = CablePath
        fields = [
            'id', 'name', 'start_device', 'start_port',
            'end_device', 'end_port', 'segments',
            'path_length', 'is_complete', 'display'
        ]
        read_only_fields = [
            'segments', 'path_length', 'is_complete'
        ]

class TraceResultSerializer(serializers.Serializer):
    """
    Сериализатор для результатов трассировки
    """
    start_device = NestedDeviceSerializer()
    start_port = NestedPowerPortSerializer()
    end_device = NestedDeviceSerializer()
    end_port = NestedPowerPortSerializer()
    segments = serializers.ListField(
        child=serializers.DictField()
    )
    length = serializers.IntegerField()
    complete = serializers.BooleanField()

    def to_representation(self, instance):
        """
        Преобразует результат трассировки в формат API
        """
        return {
            'start_device': instance['start_device'],
            'start_port': instance['start_port'],
            'end_device': instance.get('end_device'),
            'end_port': instance.get('end_port'),
            'segments': instance.get('segments', []),
            'length': len(instance.get('segments', [])),
            'complete': instance.get('complete', False)
        }