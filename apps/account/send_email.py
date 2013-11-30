#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.header import Header


def sendEmailHtml(email_type, ctx, to, _group=None):
    if email_type == 1:
        subject = ctx['username'] + " Bienvenido!"
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_activate_account.html')
    elif email_type == 2:
        subject = u"%s te invitó a %s"%( ctx['username'], unicode(settings.PROJECT_NAME,'utf-8'))
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_project_invitation.html')
    else:
        plaintext = get_template('emailtest.txt')
        htmly = get_template('emailtest.html')
        subject, to = 'Mensaje de prueba', ['no-reply@daiech.com']
    from_email = settings.FROM_EMAIL
    d = Context(ctx)
    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    try:
        smtp = settings.GMAIL_USER_PASS and settings.GMAIL_USER
    except NameError:
        smtp = None
    if smtp:
        sendGmailEmail(to, subject, html_content)
        try:
            pass
        except Exception, e:
            print "Exception sendGmailEmail", e
    else:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception, e:
            print e
            print "Error al enviar correo electronico tipo: ", email_type, " con plantilla HTML."


def sendGmailEmail(to, subject, text, attach=False):
    gmail_user = settings.GMAIL_USER
    gmail_pwd = settings.GMAIL_USER_PASS
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = ",".join(to)
    # msg['Subject'] = subject
    msg['Subject'] = "%s" % Header(subject, 'utf-8')

    # msg.attach(MIMEText(text, "html"))
    msg.attach(MIMEText(text, "html", 'utf-8'))

    if attach:
        from email import Encoders
        from email.MIMEBase import MIMEBase
        import os
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()