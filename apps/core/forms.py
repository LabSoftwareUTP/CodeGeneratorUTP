#encoding:utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
IMPORT_FILE_TYPES = ['.sql', ]


class ImportSQLForm(forms.Form):
    import_file = forms.FileField(
					required= True,
					label= _(u"Selecione el archivo MySQL (.sql)")
				)

    def clean_import_file(self):
    	import os
        import_file = self.cleaned_data['import_file']
        extension = os.path.splitext( import_file.name )[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s no es un archivo válido.' % extension )
        else:
            return import_file
