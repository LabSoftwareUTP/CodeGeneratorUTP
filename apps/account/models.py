#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


class activation_keys(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    email = models.CharField(max_length=150, verbose_name="Email")
    activation_key = models.CharField(max_length=150, verbose_name="Activation_key")
    date_generated = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s %s" % (self.email, self.activation_key, self.is_expired)
