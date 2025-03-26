from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import CablePath, PathSegment
from dcim.api.serializers import NestedDeviceSerializer, NestedPowerPortSerializer, NestedInterfaceSerializer

class PathSegmentSerializer(NetBoxModelSerializer):
    cable = serializers.HyperlinkedIdentityField(view_name='dcim-api:cable-detail')
    device_a = NestedDeviceSerializer()
    port_a = serializers.SerializerMethodField()
    device_b = NestedDeviceSerializer()
    port_b = serializers.SerializerMethodField()

    class Meta:
        model = PathSegment
        fields = [
            'id', 'cable', 'sequence', 
            'device_a', 'port_a', 
            'device_b', 'port_b',
            'display'
        ]

    def get_port_a(self, obj):
        if obj.port_a_type == 'PowerPort':
            return NestedPowerPortSerializer(obj.port_a).data
        elif obj.port_a_type == 'Interface':
            return NestedInterfaceSerializer(obj.port_a).data

    def get_port_b(self, obj):
        if obj.port_b_type == 'PowerPort':
            return NestedPowerPortSerializer(obj.port_b).data
        elif obj.port_b_type == 'Interface':
            return NestedInterfaceSerializer(obj.port_b).data


class CablePathSerializer(NetBoxModelSerializer):
    start_device = NestedDeviceSerializer()
    start_port = serializers.SerializerMethodField()
    end_device = NestedDeviceSerializer()
    end_port = serializers.SerializerMethodField()
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
        read_only_fields = ['segments', 'path_length', 'is_complete']

    def get_start_port(self, obj):
        if obj.start_port_type == 'PowerPort':
            return NestedPowerPortSerializer(obj.start_port).data
        elif obj.start_port_type == 'Interface':
            return NestedInterfaceSerializer(obj.start_port).data

    def get_end_port(self, obj):
        if obj.end_port_type == 'PowerPort':
            return NestedPowerPortSerializer(obj.end_port).data
        elif obj.end_port_type == 'Interface':
            return NestedInterfaceSerializer(obj.end_port).data
