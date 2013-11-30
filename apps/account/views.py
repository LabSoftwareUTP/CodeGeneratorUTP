#encoding:utf-8
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext  
#Django Auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm 

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from django.core.urlresolvers import reverse
from apps.account.forms import RegisterForm, LoginCaptchaForm
from .send_email import sendEmailHtml
from hashlib import sha256 as sha_constructor
from django.contrib.auth.models import User
from django.conf import settings
import random
from django.http import Http404


@login_required()
def personal_data(request):
    return render(request, 'personal_data.html')


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


def getActivationKey(email_user):
    return sha_constructor(sha_constructor(str(random.random())).hexdigest()[:5] + email_user).hexdigest()


def set_activation_key(user):
    try:
        from .models import activation_keys
        ak_obj = activation_keys(id_user=user, email=user.email, activation_key=getActivationKey(user.email))
        ak_obj.save()
        return ak_obj
    except Exception, e:
        print "Error in activation_keys:", e
        return False


def newUser(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse("personal_data"))
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email_user = form.cleaned_data['email']
            name_newuser = form.cleaned_data['username']
            activation_key = getActivationKey(email_user)
            new_user = form.save()
            new_user.is_active = False
            new_user.username = new_user.username.replace(" ", "-")
            try:
                new_user.save()
                from models import activation_keys
                activation_keys(id_user=new_user, email=email_user, activation_key=activation_key).save()
                print reverse("activate_account", args=(activation_key,))
                ctx = {
                    "PROJECT_NAME": settings.PROJECT_NAME,
                    "URL_BASE": settings.URL_BASE,
                    'username': name_newuser, 'activation_key': activation_key
                }
                sendEmailHtml(1, ctx, [str(email_user)])  # Envio de correo con clave de activacion
                return render_to_response('registered.html', {'email_address': email_user}, context_instance=RequestContext(request))
            except Exception, e:
                print e
                return HttpResponseRedirect('/#Error-de-registro-de-usuario')
    else:
        form = RegisterForm()
    return render_to_response('newUser.html', locals(), context_instance=RequestContext(request))

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
        if not request.user.is_authenticated():
            return password_reset_done(request, template_name='password_reset_done.html')
        else:
            return HttpResponseRedirect(reverse("personal_data"))


def password_reset_confirm2(request, uidb36, token):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        if not request.user.is_authenticated():
                print "entro a password_reset_confirm2"
                return password_reset_confirm(request, uidb36, token, template_name='password_reset_confirm.html', post_reset_redirect=reverse("password_reset_done2"))
        else:
                print "no entro a password_reset_confirm2"
                return HttpResponseRedirect(reverse("personal_data"))
##




def activationKeyIsValid(activation_key):
    from apps.account.models import activation_keys
    try:
        return activation_keys.objects.get(activation_key=activation_key, is_expired=False)
    except activation_keys.DoesNotExist:
        return False
    except Exception:
        return False


def confirm_account(request, activation_key, is_invited=False):
    ak = activationKeyIsValid(activation_key)
    if ak:
        return HttpResponseRedirect(reverse("activate_account", args=(activation_key,)) + "?is_invited=1")
    else:
        return render_to_response('invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account(request, activation_key):
    if activate_account_now(request, activation_key):
        is_invited = request.GET.get('is_invited') if "is_invited" in request.GET and request.GET.get("is_invited") != "" else False
        return render_to_response('account_actived.html', {"invited": is_invited}, context_instance=RequestContext(request))
    else:
        return render_to_response('invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account_now(request, activation_key):
    from .models import activation_keys
    try:
        activation_obj = activation_keys.objects.get(activation_key=activation_key)
        if not activation_obj.is_expired:
            print "ENTRANDO"
            user = User.objects.get(id=activation_obj.id_user.pk)
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            activation_obj.is_expired = True
            activation_obj.save()
            print activation_obj
            print "SALIENDO"
            return True
        else:
            return False
    except activation_keys.DoesNotExist, e:
        print e
        return False
    except Exception, e:
        print e
        return False


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
        print request.POST
        if "captcha_0" in request.POST:
            form = LoginCaptchaForm(data=request.POST)
        else:
            form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            LOGIN_TRIES = request.session.get('LOGIN_TRIES')
            if LOGIN_TRIES:
                del request.session['LOGIN_TRIES']
            return userLogin(request, request.POST['username'], request.POST['password'])
        else:
            LOGIN_TRIES = request.session.get('LOGIN_TRIES')
            if LOGIN_TRIES:
                request.session['LOGIN_TRIES'] = LOGIN_TRIES + 1
            else:
                request.session['LOGIN_TRIES'] = 1
            if LOGIN_TRIES >= 3:
                form = LoginCaptchaForm(data=request.POST)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', locals())


@login_required()
def log_out(request):
    try:
        logout(request)
    except Exception, e:
        print e
    return HttpResponseRedirect(reverse("home"))



@login_required()
def admin_users(request):
    if request.user.is_superuser:
        from apps.account.forms import UserForm
        if request.method == 'POST':
            user_form  = UserForm(request.POST)
            u = user_form.is_valid()
            if u:
                _user = user_form.save()
                _user.is_active = False
                _user.save()
                user_form = UserForm()
            else:
                show_form = True
            if '_createanother' in request.POST:
                show_form = True
        else:
            user_form  = UserForm()
        form_mode  = "_create"
        users = User.objects.exclude(pk=1).filter()
        user_obj = False
        pk = str(request.GET.get("user")) if "user" in request.GET and request.GET.get("user") != "" else "0"
        return render_to_response("user_crud.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

@login_required()
def read_user(request, id_user):
    if request.user.is_superuser:
        u = get_object_or_404(User, pk=id_user)
        return render_to_response("users/read_user.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

@login_required()
def update_user(request, id_user):
    if request.user.is_superuser:
        _user = get_object_or_404(User, pk=id_user)
        from apps.account.forms import UserForm
        if request.method == "POST":
            user_form  = UserForm(request.POST, instance=_user)
            if user_form.is_valid():
                _user = user_form.save()
                user_form = UserForm()
                # GET vars
                u = str(request.POST.get("pk_user")) if "pk_user" in request.POST and request.POST.get("pk_user") != "" else None
                next = str("&next=" + request.POST.get("next")) if "next" in request.POST and request.POST.get("next") != "" else ""
                u = "?user=" + u if u else ""
                return HttpResponseRedirect(reverse(admin_users) + str(u) + str(next))
            else:
                show_form = True
        else:
            show_form = True
            user_form  = UserForm(instance=_user)
        form_mode = "_update"
        user_obj = _user
        return render_to_response("user_crud.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404


@login_required()
def delete_user(request, id_user):
    if request.user.is_superuser:
        _user = get_object_or_404(User, pk=id_user)
        _user.delete()
        return HttpResponseRedirect(reverse("admin_users") + "#usuario-eliminado")
    else:
        raise Http404


@login_required()
def permission_login(request, id_user):
    if request.user.is_superuser:
        _user = get_object_or_404(User, pk=id_user)
        if _user.email:
            ak_obj = set_activation_key(_user)
            if ak_obj:
                activation_key = ak_obj.activation_key
                _user.set_password(activation_key[:8])
                print settings.URL_BASE + reverse("confirm_account", args=(activation_key, activation_key[5:20]))
                email_ctx = {
                    "PROJECT_NAME": settings.PROJECT_NAME,
                    "PROJECT_DESCRIPTION": settings.PROJECT_DESCRIPTION,
                    "username": request.user.get_full_name(),
                    "newuser_username": _user.username,
                    "pass": activation_key[:8],
                    "link": settings.URL_BASE + reverse("confirm_account", args=(activation_key, activation_key[5:20])),
                }
                sendEmailHtml(2, email_ctx, [_user.email])
                _user.save()
            else:
                return HttpResponseRedirect(reverse("admin_users") + "?user=" + str(_user.id) + "&msj=Error-no-se-envio-coreo")
        else:
            return HttpResponseRedirect(reverse("admin_users") + "?user=" + str(_user.id) + "&msj=no-tiene-correo")
        return HttpResponseRedirect(reverse("admin_users")  + "?user=" + str(_user.id) + "&msj=ahora-puede-iniciar")
    else:
        raise Http404