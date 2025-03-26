from django.contrib.contenttypes.models import ContentType
from dcim.models import Cable, PowerPort, PowerOutlet
from collections import deque

def trace_cable_path(start_port):
    """
    Трассирует путь кабеля от начального порта до конечной точки
    Возвращает список сегментов пути
    """
    visited = set()
    path = []
    current_port = start_port
    
    while True:
        if current_port.id in visited:
            break
        visited.add(current_port.id)
        
        # Получаем кабель, подключенный к текущему порту
        cable = Cable.objects.filter(
            _terminations__object_id=current_port.id,
            _terminations__content_type=ContentType.objects.get_for_model(current_port)
        ).first()
        
        if not cable:
            break
            
        # Находим противоположный конец кабеля
        for termination in cable._terminations.all():
            if termination.object_id != current_port.id:
                term_model = termination.content_type.model_class()
                other_end = term_model.objects.get(id=termination.object_id)
                
                path.append({
                    'cable': cable,
                    'port_a': current_port,
                    'port_b': other_end,
                    'device_a': current_port.device,
                    'device_b': other_end.device if hasattr(other_end, 'device') else None
                })
                
                # Если это выходная розетка, ищем подключенный к ней порт
                if isinstance(other_end, PowerOutlet):
                    connected_port = PowerPort.objects.filter(
                        _connected_ports__object_id=other_end.id,
                        _connected_ports__content_type=ContentType.objects.get_for_model(other_end)
                    ).first()
                    if connected_port:
                        current_port = connected_port
                        break
                else:
                    current_port = None
                break
        else:
            break
            
        if not current_port:
            break
            
    return path
