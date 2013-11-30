from django.core.serializers import serialize
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

def jsonify(object):
    return mark_safe(serialize('json', object))

register.filter('jsonify', jsonify)
jsonify.is_safe = True

