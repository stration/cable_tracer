# api/views.py
from rest_framework.decorators import action
from rest_framework.response import Response
from dcim.models import PowerPort
from .serializers import CablePathSerializer

class CableTracertViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def trace(self, request):
        port_id = request.query_params.get('port_id')
        if not port_id:
            return Response({'error': 'port_id parameter is required'}, status=400)
            
        try:
            port = PowerPort.objects.get(id=port_id)
        except PowerPort.DoesNotExist:
            return Response({'error': 'PowerPort not found'}, status=404)
            
        path = trace_cable_path(port)
        serializer = CablePathSerializer({
            'start_device': port.device,
            'start_port': port,
            'segments': path,
            'end_device': path[-1]['device_b'] if path else None,
            'end_port': path[-1]['port_b'] if path else None
        })
        
        return Response(serializer.data)