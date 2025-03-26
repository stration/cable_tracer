from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from dcim.models import PowerPort
from ..utils.tracer import trace_cable_path
from .serializers import TraceResultSerializer

class CableTracertViewSet(ViewSet):
    def trace(self, request):
        port_id = request.query_params.get('port_id')
        if not port_id:
            return Response({'error': 'port_id parameter is required'}, status=400)
            
        try:
            port = PowerPort.objects.get(id=port_id)
        except PowerPort.DoesNotExist:
            return Response({'error': 'PowerPort not found'}, status=404)
            
        path = trace_cable_path(port)
        result = {
            'start_device': port.device,
            'start_port': port,
            'segments': path,
            'complete': False
        }
        
        if path:
            last_segment = path[-1]
            result['end_device'] = last_segment.get('device_b')
            result['end_port'] = last_segment.get('port_b')
            result['complete'] = True if not isinstance(last_segment['port_b'], PowerOutlet) else False
            
        serializer = TraceResultSerializer(result)
        return Response(serializer.data)
