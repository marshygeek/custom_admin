from django.template.defaulttags import register

from custom_admin.config import COLS_TO_SHORTEN


@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter(name='format')
def format_string(string, arg):
    return string.format(arg)


@register.filter(name='need_to_shorten')
def need_to_shorten(col_name):
    return col_name in COLS_TO_SHORTEN


@register.filter(name='shorten_col')
def shorten_col(col_name):
    half_len = len(col_name) // 2
    return '{}\n{}'.format(col_name[:half_len], col_name[half_len:])
