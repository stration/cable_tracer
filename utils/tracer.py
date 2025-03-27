from django.contrib.contenttypes.models import ContentType
from dcim.models import Cable, PowerPort, PowerOutlet, PowerFeed
from collections import deque

def trace_cable_path(start_port):
    """
    Трассировка кабеля с учетом особенностей NetBox 4.2.6
    Поддерживает PowerPort -> PowerOutlet -> PowerPort -> PowerFeed
    """
    path = []
    current_termination = start_port
    visited = set()

    while current_termination:
        if current_termination.id in visited:
            # Обнаружен цикл
            break
        visited.add(current_termination.id)

        # Получаем кабель, подключенный к текущей точке
        cable = Cable.objects.filter(
            _terminations__object_id=current_termination.id,
            _terminations__content_type=ContentType.objects.get_for_model(current_termination)
        ).first()

        if not cable:
            # Если нет кабеля, завершаем трассировку
            break

        # Находим противоположный конец кабеля
        other_end = None
        for termination in cable.terminations.all():
            if termination.id != current_termination.id:
                other_end = termination
                break

        if not other_end:
            # Если нет противоположного конца, завершаем трассировку
            break

        # Формируем сегмент пути
        segment = {
            'cable': cable,
            'a_side': current_termination,
            'b_side': other_end,
            'device_a': getattr(current_termination, 'device', None),
            'device_b': getattr(other_end, 'device', None)
        }
        path.append(segment)

        # Определяем следующую точку трассировки
        if isinstance(other_end, PowerOutlet):
            # Ищем подключенный PowerPort
            next_port = PowerPort.objects.filter(
                _connected_port__object_id=other_end.id,
                _connected_port__content_type=ContentType.objects.get_for_model(other_end)
            ).first()
            current_termination = next_port
        elif isinstance(other_end, PowerFeed):
            # Конец трассировки - достигли PowerFeed
            break
        else:
            # Для других типов завершаем трассировку
            break

    return path
