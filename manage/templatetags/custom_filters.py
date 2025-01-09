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
