from dcim.models import Cable, PowerPort, PowerOutlet, Interface
from collections import deque
from django.contrib.contenttypes.models import ContentType

def trace_cable_path(start_port):
    """
    Трассирует путь кабеля от начального порта до конечной точки
    """
    visited = set()
    path = []
    queue = deque([(start_port, [])])

    while queue:
        current_port, current_path = queue.popleft()

        # Проверка на циклы
        if current_port.id in visited:
            continue
        visited.add(current_port.id)

        # Получаем все кабели, подключенные к текущему порту
        cables = Cable.objects.filter(
            _terminations__object_id=current_port.id,
            _terminations__content_type=ContentType.objects.get_for_model(current_port)
        ).prefetch_related('_terminations')

        if not cables:
            # Конечная точка пути
            return current_path

        for cable in cables:
            # Находим противоположный конец кабеля
            for termination in cable._terminations.all():
                if termination.object_id != current_port.id:
                    term_model = termination.content_type.model_class()
                    other_end = term_model.objects.get(id=termination.object_id)

                    new_path = current_path + [{
                        'cable': cable,
                        'port_a': current_port,
                        'port_b': other_end,
                        'device_a': current_port.device,
                        'device_b': other_end.device if hasattr(other_end, 'device') else None
                    }]

                    # Если это выходная розетка, ищем подключенный к ней порт
                    if isinstance(other_end, PowerOutlet):
                        connected_port = PowerPort.objects.filter(
                            _connected_ports__object_id=other_end.id,
                            _connected_ports__content_type=ContentType.objects.get_for_model(other_end)
                        ).first()
                        if connected_port:
                            queue.append((connected_port, new_path))
                    elif isinstance(other_end, Interface):
                        # Добавляем поддержку сетевых интерфейсов
                        queue.append((other_end, new_path))
                    else:
                        # Если нет дальнейших подключений, завершаем путь
                        return new_path

    return path
