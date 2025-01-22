import ast
import json

from django import template

register = template.Library()


@register.filter(name='color_suits')
def color_suits(text):
    if not text:
        return text

    colored_text = text.replace('♠', '<span class="spade">♠</span>') \
        .replace('♥', '<span class="heart">♥</span>') \
        .replace('♦', '<span class="diamond">♦</span>') \
        .replace('♣', '<span class="club">♣</span>') \
        .replace('\\n', '<br>')

    return colored_text


@register.filter
def get_item(dictionary, key):
    if isinstance(key, int):
        return dictionary.get(key) or dictionary.get(str(key))
    return dictionary.get(key)


@register.filter(name='modify_bids')
def modify_bids(value):
    if not isinstance(value, str):
        return value  # Ensure the value is a string before processing
    
    # Replace "P", "DBL", and "RDBL"
    value = value.replace("P", "P  ")
    value = value.replace("DBL", "X  ")
    value = value.replace("RDBL", "XX ")

    suits = ['♥', '♦', '♣', '♠']
    for suit in suits:
        value = value.replace(suit, suit + ' ')
    return value


@register.filter(name='split_newline')
def split_newline(value):
    if isinstance(value, str):
        # Normalize \\n to \n and then split by \n
        normalized_value = value.replace('\\n', '\n')
        return normalized_value.split('\n')
    return value


@register.filter
def is_dict(value):
    try:
        parsed_value = ast.literal_eval(value) if isinstance(value, str) else value
        return isinstance(parsed_value, dict)
    except (ValueError, SyntaxError):
        return False


@register.filter
def dict_get(value, key):
    parsed_value = ast.literal_eval(value) if isinstance(value, str) else value
    return parsed_value.get(key) if isinstance(parsed_value, dict) else None


@register.filter
def is_convertible_to_dict(value):
    try:
        json.loads(value)
        return True
    except (ValueError, TypeError):
        return False


@register.filter
def mul(value, multiplier):
    try:
        return value * multiplier
    except (TypeError, ValueError):
        return None
