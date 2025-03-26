from rest_framework.decorators import action
from rest_framework.response import Response
from dcim.models import PowerPort, Interface
from .serializers import CablePathSerializer
from .utils.tracer import trace_cable_path

class CableTracertViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def trace(self, request):
        port_id = request.query_params.get('port_id')
        port_type = request.query_params.get('port_type', 'PowerPort')  # По умолчанию PowerPort

        if not port_id or not port_type:
            return Response({'error': 'port_id and port_type parameters are required'}, status=400)

        try:
            if port_type == 'PowerPort':
                port = PowerPort.objects.get(id=port_id)
            elif port_type == 'Interface':
                port = Interface.objects.get(id=port_id)
            else:
                return Response({'error': 'Invalid port_type'}, status=400)
        except (PowerPort.DoesNotExist, Interface.DoesNotExist):
            return Response({'error': 'Port not found'}, status=404)

        path = trace_cable_path(port)

        serializer = CablePathSerializer({
            'start_device': port.device,
            'start_port': port,
            'segments': path,
            'end_device': path[-1]['device_b'] if path else None,
            'end_port': path[-1]['port_b'] if path else None
        })
        return Response(serializer.data)
