
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from shows.models import Show, Episode
import os

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
        self.object.deleted_at = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.success_url)

@method_decorator(login_required, name='get')
class EpisodeList(ListView):
    template_name = 'episodes/index.html'
    model = Episode
    paginate_by = 20
    
    def get_queryset(self):
        self.show = get_object_or_404(Show, id=self.kwargs['pk'])
        return Episode.objects.filter(show=self.show, deleted_at=None)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the show
        context['show'] = self.show
        return context

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class EpisodeCreate(CreateView):
    template_name = 'episodes/form.html'
    model = Episode
    fields = ['title', 'description', 'cover']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.show = get_object_or_404(Show, id=self.kwargs['pk'])
        context['show'] = self.show
        context['form_type'] = settings.GLOBAL_SETTINGS['FORM_CREATE']
        context.update(settings.GLOBAL_SETTINGS)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.show = get_object_or_404(Show, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.show = self.show
        form.instance.created_at = timezone.now()
        form.instance.updated_at = timezone.now()
        # Save model
        self.object = form.save()
        # Save file into the model directory
        self.object.cover.save(os.path.basename(self.object.cover.name), self.object.cover, save=True)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self, **kwargs):
        show = self.object.show 
        return reverse_lazy('episodes.list', kwargs={'pk': show.id})

@method_decorator(login_required, name='get')
class EpisodeDetail(DetailView):
    template_name = 'episodes/form.html'
    model = Episode
    fields = ['title', 'description', 'cover']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = settings.GLOBAL_SETTINGS['FORM_SHOW']
        context['readonly'] = 'readonly'
        context['disabled'] = 'disabled'
        context.update(settings.GLOBAL_SETTINGS)
        return context

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class EpisodeUpdate(UpdateView):
    template_name = 'episodes/form.html'
    model = Episode
    fields = ['title', 'description', 'cover']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = settings.GLOBAL_SETTINGS['FORM_EDIT']
        context.update(settings.GLOBAL_SETTINGS)
        return context
    
    def get_success_url(self, **kwargs):
        show = self.object.show 
        return reverse_lazy('episodes.list', kwargs={'pk': show.id})

@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class EpisodeDelete(DeleteView):
    model = Episode
    
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted_at = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self, **kwargs):
        show = self.object.show 
        print(show)
        return reverse_lazy('episodes.list', kwargs={'pk': show.id})

