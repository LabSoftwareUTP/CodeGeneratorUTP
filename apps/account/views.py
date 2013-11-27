#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext  
#Django Auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm 

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from django.core.urlresolvers import reverse
from apps.account.forms import RegisterForm


@login_required()
def personal_data(request):
    return render_to_response('personal_data.html', context_instance=RequestContext(request))


@login_required()
def update_personal_data(request):
    from apps.account.forms import UserForm
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            _user = user_form.save()
            update = True
            user_form = False  # don't show the form
        else:
            update = False
    else:
        user_form = UserForm(instance=request.user)
        update = False
    return render_to_response('personal_data.html', locals(), context_instance=RequestContext(request))


##
@login_required()
def changePassword(request):
    passUpdate = False
    if request.method == "POST":
        passUpdate = False
        passForm = PasswordChangeForm(data=request.POST, user=request.user)
        if passForm.is_valid():
            passForm.save()
            passUpdate = True
    else:
        passForm = PasswordChangeForm(user=request.user)
        passUpdate = False
    ctx = {"passForm": passForm, "dataUpdate": False, "passwordUpdate": passUpdate, "error_email": False}
    return render_to_response('password.html', ctx, context_instance=RequestContext(request))


def password_reset_complete2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        if not request.user.is_authenticated():
            return password_reset_complete(request, template_name='password_reset_complete.html')
        else:
            print "no entro a password_reset_complete2"
            return HttpResponseRedirect(reverse("personal_data"))


def password_reset2(request):
        """
        django.contrib.auth.views.password_reset view (forgotten password)
        """
        saveViewsLog(request, "account.views.password_reset2")
        if not request.user.is_authenticated():
            print "entro a password_reset2"
            try:
                return password_reset(request, template_name='password_reset_form.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt', post_reset_redirect=reverse("password_reset_done2"))
            except Exception:
                return HttpResponseRedirect(reverse("password_reset_done2"))
        else:
            print "no entro a password_reset2"
            return HttpResponseRedirect(reverse("personal_data"))


def password_reset_done2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_done2")
        if not request.user.is_authenticated():
            return password_reset_done(request, template_name='password_reset_done.html')
        else:
            return HttpResponseRedirect(reverse("personal_data"))


def password_reset_confirm2(request, uidb36, token):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_confirm2")
        if not request.user.is_authenticated():
                print "entro a password_reset_confirm2"
                return password_reset_confirm(request, uidb36, token, template_name='password_reset_confirm.html', post_reset_redirect=reverse("password_reset_done2"))
        else:
                print "no entro a password_reset_confirm2"
                return HttpResponseRedirect(reverse("personal_data"))
##



def userLogin(request, user_name, password):
    try:
        next = request.GET['next']
    except Exception:
        next = '/'
    access = authenticate(username=user_name, password=password)
    if access is not None:
        if access.is_active:
            login(request, access)
            return HttpResponseRedirect(next)
        else:
            return render_to_response('no_active.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login') + '?next=' + next)



def log_in(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse("personal_data"))
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return userLogin(request, request.POST['username'], request.POST['password'])
    else:
        form = AuthenticationForm()
    return render_to_response('login.html', locals(), context_instance=RequestContext(request))


@login_required()
def log_out(request):
    try:
        logout(request)
    except Exception, e:
        print e
    return HttpResponseRedirect(reverse("home"))
