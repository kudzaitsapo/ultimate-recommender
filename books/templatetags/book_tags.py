from django import template

register = template.Library()


@register.simple_tag
def is_user_liked_book(book, user_id):
    return book.has_user_liked_book(user_id)
