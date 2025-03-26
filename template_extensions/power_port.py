# template_extensions/power_port.py
from extras.plugins import TemplateExtension
from .models import CablePath

class PowerPortTracertButton(TemplateExtension):
    model = 'dcim.powerport'
    
    def buttons(self):
        return f"""
        <a href="{% url 'plugins:cable_tracert:trace' port_id={self.context['object'].pk} %}" class="btn btn-primary btn-sm">
            <i class="mdi mdi-transit-connection-variant"></i> Трассировать кабель
        </a>
        """