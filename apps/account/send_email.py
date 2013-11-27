#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context,  RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import json


def sendEmailHtml(email_type, ctx, to, _group=None):
    if email_type == 1:
        subject = ctx['username'] + " Bienvenido!"
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_activate_account.html')
    else:
        plaintext = get_template('emailtest.txt')
        htmly = get_template('emailtest.html')
        subject, to = 'Mensaje de prueba', ['no-reply@daiech.com']
    from_email = settings.FROM_EMAIL
    d = Context(ctx)
    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        print "Mensaje enviado"
    except:
        print "Error al enviar correo electronico tipo: ", email_type
       