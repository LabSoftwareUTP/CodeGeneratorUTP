from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).distinct()

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class DataBaseTmp(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user')
    db_name = models.CharField(max_length=100,verbose_name=_("Nombre de la db"))
    filename = models.CharField(max_length=100,verbose_name=_("Nombre de archivo"))
    media_filename = models.CharField(max_length=100,verbose_name=_("Nombre de archivo"))
    objects = GenericManager()

    is_deleted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s ---> deleted:%s" % (self.user, self.db_name, self.is_deleted)
