from random import choice
from django import template

register = template.Library()

@register.simple_tag
def rand_tw_clr():
    return choice([
        "bg-rose-400",
        "bg-amber-400",
        "bg-lime-400",
        "bg-green-400",
        "bg-orange-400",
        "bg-yellow-400",
        "bg-violet-400",
        "bg-purple-400",
        "bg-indigo-400",
        "bg-sky-400",
        "bg-pink-400"
    ])




