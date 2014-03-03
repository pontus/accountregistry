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



logger = logging.getLogger(__name__)


def index(request):

    #t = loader.get_template('register/main.tmpl')
    #c = Context({
    #    'a': 10
    #})
    return render_to_response('register/main.tmpl', {'a':10})

def logout_view(request):
    logout(request)
    return render_to_response('register/loggedout.tmpl', {'a':10})





















class servicesForm(forms.Form):


    #hej = forms.BooleanField(required=False, label='Test.')

    def __init__(self, *args, **kwargs):

        
        # Show form for all our services
        forms.Form.__init__(self, *args, **kwargs)
        for p in register.models.service.objects.all():

            if p.tag not in self.fields.keys():
                self.fields[p.tag] =  forms.BooleanField(required=False, label=p.description)


            #openstack = forms.BooleanField(required=False, label='The OpenStack cloud service')
            #fido = forms.BooleanField(required=False, label='The FIDO service provision system')

        #logger.debug(repr(dir(self)))
        #logger.debug(repr(self.fields))

class passwordForm(forms.Form):
    password = forms.CharField(label='New password')


@login_required
def request(request):

    sForm = servicesForm()
    pwdForm = passwordForm()

    c = {'email': request.user.email,
         'name': '%s %s' % (request.user.first_name, request.user.last_name) + " "+ repr(servicesForm),
         'servicesForm': sForm,
         'passwordForm': pwdForm,
         'current_request': False}

    c.update(csrf(request))

    has_account = request.session.get('has_account')
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



def request_sent(request):
    
    c = {}

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
            
            newpwd = f2.cleaned_data['password']          
            
            if register.account.exists(request.user.email):
                register.account.changepwd(request.user.email, newpwd)

                                               
        
    return render_to_response('register/request_done.tmpl', c)
