# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse
import register.models

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth import logout

from django import forms

import register.account
import logging

import djangosaml2.views


logger = logging.getLogger(__name__)


def index(request):

    #t = loader.get_template('register/main.tmpl')
    #c = Context({
    #    'a': 10
    #})
    return render_to_response('register/main.tmpl', {})

def logout_view(request):
    logout(request)
    return render_to_response('register/loggedout.tmpl', {})




def login_view(request):
    return djangosaml2.views.login(request, wayf_template='register/wayf.tmpl')
    













class servicesForm(forms.Form):

    def __init__(self, *args, **kwargs):

        
        # Show form for all our services
        forms.Form.__init__(self, *args, **kwargs)
        for p in register.models.service.objects.all():

            if p.tag not in self.fields.keys():
                self.fields[p.tag] =  forms.BooleanField(required=False, label=p.description)

class passwordForm(forms.Form):
    password = forms.CharField(label='New password')


@login_required
def request(request):

    sForm = servicesForm()
    pwdForm = passwordForm()

    c = {'email': request.user.email,
         'name': '%s %s' % (request.user.first_name, request.user.last_name),
         'servicesForm': sForm,
         'passwordForm': pwdForm,
         'current_request': False}

    c.update(csrf(request))

    # Offer password change?
    has_account = request.session.get('has_account')
    c.update({'has_account':True})

    logger.debug(request.user.email+ ' has_account '+repr(has_account))

    if not has_account:
        has_account = register.account.exists(request.user.email)
        if has_account:
            request.session['has_account'] = True
            c.update({'has_account':True})
        
    
    if register.models.request.objects.filter(email=request.user.email):
        c['current_request'] = True

    #t = loader.get_template('register/main.tmpl')
    #c = Context({
    #    'a': 10
    #})
    return render_to_response('register/request.tmpl', c)


@login_required
def request_sent(request):
    
    c = {}

    try:
        if request.method == 'POST':
            f1 = servicesForm(request.POST)
            f2 = passwordForm(request.POST)

            if f1.is_valid():

                logger.debug("f1 "+repr(f1.fields.keys()))

                c['services_change'] = False

                g = f1.cleaned_data

                srv = ' '.join( filter(lambda(x) : g[x], g.keys()))
                user_requests = register.models.request.objects.filter(email=request.user.email)

                if not user_requests:
                    r = register.models.request.objects.create()
                else:
                    r = user_requests[0]

                r.email = request.user.email
                r.name = '%s %s' % (request.user.first_name, request.user.last_name)

                if r.services != srv:
                    r.services = srv
                    c['services_change'] = True

                r.message = ''
                r.save()

            if f2.is_valid():
            
                c['pw_change'] = True     
            
                newpwd = str(f2.cleaned_data['password'])
                logger.debug('pwd: '+newpwd)

                if register.account.exists(request.user.email):
                    register.account.changepwd(request.user.email, newpwd)
    except:
        return render_to_response('register/request_failed.tmpl', c)
                                               
        
    return render_to_response('register/request_done.tmpl', c)


class requestsForm(forms.Form):

    def __init__(self, *args, **kwargs):

        
        # Show form for all our services
        forms.Form.__init__(self, *args, **kwargs)
        for p in register.models.request.objects.all():

            self.fields[p.email] = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple,
                                                             choices=( 
                ('reject', 'Reject'), ('grant', 'Grant')), 
                                                             label="%s (%s) requested %s with extra message: %s" % 
                                                             (p.email, p.name, p.services, p.message),
                                                             required=False)



@login_required
def admin_view(request):
    
    adminuser = False
    admins =  register.models.admins.objects.all()

    currentuser = request.user.email.lower()

    for p in admins:
        if p.email.lower() == currentuser:
            adminuser = True

    if not adminuser:
        c['admin_failed'] = True
        return render_to_response('register/request_failed.tmpl', c)

    c = {}
    c.update(csrf(request))

    c['requests'] = requestsForm() # register.models.request.objects.all()

    return render_to_response('register/admin.tmpl', c)
        

@login_required
def admin_sent(request):

    
    reqs_handled = {}
    c = { 'reqs': reqs_handled }

    #try:
    if 1:
        f = requestsForm(request.POST)

        if f.is_valid():
            for p in f.fields.keys():
                logger.debug(p+ ' response  '+repr(f.cleaned_data[p]))

                if not f.cleaned_data[p]:                   
                    reqs_handled[p] = "ignored"
                elif len(f.cleaned_data[p]) > 1:
                    reqs_handled[p] = "too many choices made, ignored"
                elif f.cleaned_data[p] == [u'reject']:
                    reqs_handled[p] = "rejected, user mail sent"

                elif f.cleaned_data[p] == [u'grant']:
                    if register.account.exists(p):
                        reqs_handled[p] = "accepted, user mail sent, user had an account already"
                    else:
                        reqs_handled[p] = "accepted, user mail sent, new account created"

                

        #account.create(request.user.email, reque_name, request.user.last_name)

    #except:
    #    return render_to_response('register/request_failed.tmpl', c)


    return render_to_response('register/admin_sent.tmpl', c)
