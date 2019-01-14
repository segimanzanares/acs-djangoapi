
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.conf import settings
from shows.models import Show
import datetime

@method_decorator(login_required, name='get')
class ShowList(ListView):
    template_name = 'shows/index.html'
    model = Show
    paginate_by = 20
    
    def get_queryset(self):
        return self.model.objects.filter(deleted_at=None)

@method_decorator(login_required, name='get')
class ShowDetail(DetailView):
    template_name = 'shows/form.html'
    model = Show
    fields = ['title']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = settings.GLOBAL_SETTINGS['FORM_SHOW']
        context['readonly'] = 'readonly'
        context['disabled'] = 'disabled'
        context.update(settings.GLOBAL_SETTINGS)
        return context

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class ShowCreate(CreateView):
    template_name = 'shows/form.html'
    model = Show
    fields = ['title']
    success_url = reverse_lazy('shows.list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = settings.GLOBAL_SETTINGS['FORM_CREATE']
        context.update(settings.GLOBAL_SETTINGS)
        return context

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class ShowUpdate(UpdateView):
    template_name = 'shows/form.html'
    model = Show
    fields = ['title']
    success_url = reverse_lazy('shows.list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = settings.GLOBAL_SETTINGS['FORM_EDIT']
        context.update(settings.GLOBAL_SETTINGS)
        return context

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class ShowDelete(DeleteView):
    model = Show
    success_url = reverse_lazy('shows.list')
    
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted_at = str(datetime.datetime.utcnow())
        self.object.save()
        return HttpResponseRedirect(self.success_url)