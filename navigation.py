from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:cable_tracer:trace',
        link_text='Cable Tracer',
        buttons=[
            PluginMenuButton(
                link='plugins:cable_tracer:trace',
                title='Trace Cable',
                icon_class='mdi mdi-connection',
                color=ButtonColorChoices.BLUE
            )
        ]
    ),
)
