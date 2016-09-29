# -*- coding: utf8 -*-
#from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from request.models import Filing
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import *
from django.shortcuts import render_to_response,redirect, render
#from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views.decorators.csrf import csrf_protect
from django_tables2 import RequestConfig


from datetime import datetime



from django.shortcuts import render


@csrf_protect
def login_user(request):
    logout(request)
    username = password = ''
    c = {}
    #c.update(csrf(request))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    #return render_to_response('login.html', context_instance=RequestContext(request))
    #return render_to_response('login.html', c)
    return render(request, 'login.html', c)

@csrf_protect
def logout_user(request):
    logout(request)
    return render(request, 'login.html')

class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = '/'
    template_name = 'filing/index.html'

    def get(self, request, *args, **kwargs):
        global tmp
        tmp = ''
        return super(IndexView, self).get(request, *args, **kwargs)


class FilterView(TemplateView):
    #login_url = '/login/'
    #redirect_field_name = '/'
    template_name = 'filing/index.html'
    dep_id = None
    date_start = None
    #first_date = None
    #last_date = None

    def get(self, request, *args, **kwargs):
        if self.kwargs["id"] == None:
            self.dep_id = 0
        else:
            self.dep_id = self.kwargs["id"]
        #global tmp
        #tmp = self.dep_id
        RequestListJson.dep_id=self.dep_id
        return super(FilterView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.date_start = request.POST.get('daterange','01.01.2016')
        RequestListJson.first_date = self.date_start[:10]
        RequestListJson.last_date = self.date_start[13:]
        #if self.kwargs["daterange"] == None:
        #    self.date_start = 0
        #else:
        #    self.date_start = self.kwargs["id"]
        #print('--------- post ------------------')
        #print(self.first_date)
        #print(self.last_date)
        #print('---------------------------')
        context = self.get_context_data()
        return super(FilterView, self).render_to_response(context)


    def get_context_data(self, ** kwargs):
        context = super(FilterView, self).get_context_data( ** kwargs)
        filter_customer = self.request.GET.get(u'id', None)


class RequestListJson(BaseDatatableView):
    model = Filing
    columns = ['apptype', 'jobtype', 'jobtext', 'ObjName', 'eqpName', 'DateReqStart', 'DateReqFinish', 'dep_name']
    order_columns = ['apptype', 'jobtype', 'jobtext', 'ObjName', 'eqpName', 'DateReqStart', 'DateReqFinish', 'dep_name']
    dep_id = None
    first_date = None
    last_date = None

    def filter_queryset(self, qs):
        qs = BaseDatatableView.filter_queryset(self, qs)
        #qs = qs.filter(DateReqStart__range=["2016-01-01","2016-09-01"])

        #if not (self.dep_id is None):
        if not (self.first_date is None):
            d1 = datetime.strptime(self.first_date,'%d.%m.%Y').date()
            d2 = datetime.strptime(self.last_date,'%d.%m.%Y').date()
            print('--------- filter_queryset ------------------')
            print(self.first_date)
            print(self.last_date)
            print('---------------------------')
            qs = qs.filter(DateReqStart__range=[d1,d2])
        #    qs = qs.filter(dep_id__istartswith=self.dep_id)
        # simple example:
        search = self.request.GET.get(u'search[value]', None)

        #if search:
        #    qs = qs.filter(dep_id__istartswith=search)
            #qs = qs.filter(name__istartswith='мисим')
        # more advanced example
        filter_customer = self.request.GET.get(u'customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        #q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
        #qs = qs.filter(dep_name__istartswith='710')
        #return BaseDatatableView.filter_queryset(self, qs)
        return qs

