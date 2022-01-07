from django import template
from django.core.serializers import serialize
import json

register = template.Library()


@register.filter(name="split")
def split(str, key):
    return str.split(key)


# @register.simple_tag(name='get_img_url')
# def get_img_url(*args, **kwargs):
#     return Post.get_image_url(*args, **kwargs)


@register.filter(name="json_serialize")
def json_serialize(value):
    return serialize("json", value)


@register.filter(name="arr_filter")
def arr_filter(arr, val):
    """
    filter array depending on provided post pk
    """
    # print("arr-filter: ", arr)
    obj = json.loads(
        json.dumps(list(filter(lambda li: li.get("pk") == val, list(json.loads(arr)))))
    )[0]

    if obj["model"]:
        del obj["model"]

    return json.dumps(obj)
