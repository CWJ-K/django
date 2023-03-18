from django import template

register = template.Library()


# @register.simple_tag
# def greet_user(message, username):
#     return '{greeting_message}, {user}!!!'.format(greeting_message=message, user=username)


@register.simple_tag(takes_context=True)
def contextual_greet_user(context, message):
    username = context['username']
    return '{greeting_message}, {user}!!!'.format(greeting_message=message, user=username)
