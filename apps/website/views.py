from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse


def home(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse("login"))
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


def update(request):
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    gitpull = commands.getstatusoutput('git pull origin master')[1]
    return HttpResponse("<pre>"+gitpull+"</pre><br><a href='" + reverse(reload) + "'>Reload Nginx</a>")


def reload(request):
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
    out = commands.getstatusoutput("ps -Af | grep uwsgi | grep -v grep | awk '{ print $2 }' | xargs kill")[1]
    out = out + commands.getstatusoutput("echo Stopped... please wait")[1]
    out = out + commands.getstatusoutput("sleep 1")[1]
    out = out + commands.getstatusoutput("uwsgi --socket :8002 --wsgi-file wsgi.py -d log.log")[1]
    out = out + commands.getstatusoutput("echo Finished...")[1]
    return HttpResponse("<pre>"+out+"</pre>")