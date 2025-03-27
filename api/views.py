from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dcim.models import PowerPort
from ..utils.tracer import trace_cable_path
from .serializers import TraceResultSerializer

class CableTraceView(APIView):
    """
    API для трассировки кабелей (NetBox 4.2.6 compatible)
    """
    def get(self, request):
        port_id = request.query_params.get('port_id')
        if not port_id:
            return Response(
                {'error': 'Parameter "port_id" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            port = PowerPort.objects.get(id=port_id)
        except PowerPort.DoesNotExist:
            return Response(
                {'error': f'PowerPort with id {port_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        path = trace_cable_path(port)
        result = {
            'start': {
                'device': port.device,
                'port': port
            },
            'path': path,
            'is_complete': bool(path) and isinstance(path[-1]['b_side'], PowerFeed)
        }

        serializer = TraceResultSerializer(result)
        return Response(serializer.data)
