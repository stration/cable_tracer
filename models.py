# models.py
from django.db import models
from netbox.models import NetBoxModel
from dcim.models import Cable, Device, PowerPort, PowerOutlet

class CablePath(NetBoxModel):
    """
    Модель для хранения полного пути кабеля от начальной до конечной точки
    """
    name = models.CharField(max_length=100)
    start_device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='start_cable_paths'
    )
    start_port = models.ForeignKey(
        to=PowerPort,
        on_delete=models.CASCADE,
        related_name='start_cable_paths'
    )
    end_device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='end_cable_paths'
    )
    end_port = models.ForeignKey(
        to=PowerPort,
        on_delete=models.CASCADE,
        related_name='end_cable_paths',
        null=True,
        blank=True
    )
    is_complete = models.BooleanField(default=False)
    path_length = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.start_device} → {self.end_device})"

class PathSegment(NetBoxModel):
    """
    Модель для хранения сегментов пути кабеля
    """
    cable_path = models.ForeignKey(
        to=CablePath,
        on_delete=models.CASCADE,
        related_name='segments'
    )
    cable = models.ForeignKey(
        to=Cable,
        on_delete=models.CASCADE,
        related_name='path_segments'
    )
    sequence = models.PositiveIntegerField()
    device_a = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='segment_a_ends'
    )
    port_a = models.ForeignKey(
        to=PowerPort,
        on_delete=models.CASCADE,
        related_name='segment_a_ends'
    )
    device_b = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
        related_name='segment_b_ends'
    )
    port_b = models.ForeignKey(
        to=PowerPort,
        on_delete=models.CASCADE,
        related_name='segment_b_ends'
    )

    class Meta:
        ordering = ['cable_path', 'sequence']
        unique_together = ['cable_path', 'sequence']

    def __str__(self):
        return f"Segment {self.sequence} of {self.cable_path}"