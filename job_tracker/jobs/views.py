from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView

from .models import Application

User = get_user_model()


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    context_object_name = 'applications'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application

    def get_object(self):
        obj = get_object_or_404(Application, slug=self.kwargs['slug']) 
        if obj.user != self.request.user:
            raise Http404()
        return obj


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    fields = [
        'name',
        'email',
        'company_name',
        'position',
        'rate',
        'status',
        'notes'
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = Application
    fields = [
        'name',
        'email',
        'company_name',
        'position',
        'rate',
        'status',
        'notes'
    ]
    action = "Update"


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    fields = [
        'name',
        'email',
        'company_name',
        'position',
        'rate',
        'status',
        'notes'
    ]
    action = "Delete"
    success_url = reverse_lazy('jobs:list')