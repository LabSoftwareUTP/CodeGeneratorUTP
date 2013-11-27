from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse


def home(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse("login"))
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

