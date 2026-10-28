from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def player_name(context, player):
    icon, title, detail = context.get('player_badges', {}).get(player.id, ('', '', ''))
    return format_html('<span title="{} · {}">{}</span> {}', title, detail, icon, player.name)
