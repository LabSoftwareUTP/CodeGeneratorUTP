from django.template import Library
from django.template import Variable, VariableDoesNotExist
from django.utils.log import getLogger

register = Library()
logger = getLogger('django')


@register.assignment_tag(takes_context=True)
def editinline(context, context_variable, **kwargs):
    try:
        field_value = Variable(context_variable).resolve(context)
    except VariableDoesNotExist:
        field_value = ''
    except Exception, e:
        field_value = ''
        print "ERROR:", e
    field_name = context_variable.split('.')[-1]
    try:
        context_obj = Variable(context_variable.split('.')[0])\
                        .resolve(context)
        request = Variable('request').resolve(context)
        

        # adaptor = get_adaptor(request, context_obj, field_name, field_value=field_value,\
        #                         kwargs=kwargs, adaptor=adaptor_str)
        # return adaptor.render()
        print "************************************************"
        print "field_value: %s, tipo %s" % (field_value, type(field_value))
        print "context_obj: %s, tipo %s" % (context_obj, type(context_obj))
        print "field_name: %s " % (field_name)
    except VariableDoesNotExist:
        logger.warning("editlive: the template variable \"%s\" doesn't exists." % context_variable)
        return u''




    print "obj type", type(context_variable)
    return field_value

# register.filter('editinline', editinline)
