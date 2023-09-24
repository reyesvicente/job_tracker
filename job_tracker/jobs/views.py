from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView

from .models import Application


class ApplicationListView(ListView):
    model = Application


class ApplicationDetailView(DetailView):
    model = Application


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
        form.instance.creator = self.request.user
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