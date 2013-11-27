from django import template
import urllib
import hashlib
from django.conf import settings

register = template.Library()


def showgravatar(email, size):
    #default = "http://cms.myspacecdn.com/cms/Music%20Vertical/Common/Images/default_small.jpg"
    default = settings.URL_BASE + "/static/img/user_default.png"

    url = "http://www.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(),
        # 'default': default,
        'size': str(size)
    })
    return url
register.filter('showgravatar', showgravatar)