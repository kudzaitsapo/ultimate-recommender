from math import ceil
from django import template

register = template.Library()


@register.filter
def as_chunks(lst, chunk_size):
    limit = ceil(len(lst) / chunk_size)
    for idx in range(limit):
        yield lst[chunk_size * idx : chunk_size * (idx + 1)]
