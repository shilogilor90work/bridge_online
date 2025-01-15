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

    # Add a space after each suit (S, H, D, C)
    value = re.sub(r'([♥♦♣♠])', r'\1 ', value)

    return value