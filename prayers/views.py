from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Prayer
from .forms import PrayerForm
from django.utils import timezone
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
decorators = [user_passes_test(lambda u:u.is_superuser)]

class PrayerListView(LoginRequiredMixin, ListView):
    model = Prayer

    def get_queryset(self):
        return Prayer.objects.filter(date__lte=timezone.now()).order_by('-date')

class PrayerDetailView(LoginRequiredMixin, DetailView):
    model = Prayer

@method_decorator(decorators, name='dispatch')
class CreatePrayerView(CreateView):
    redirect_field_name = 'index.html'
    form_class = PrayerForm
    model = Prayer


@method_decorator(decorators, name='dispatch')
class PrayerUpdateView(UpdateView):
    redirect_field_name = 'prayers/prayer_list.html'
    form_class = PrayerForm
    model = Prayer


@method_decorator(decorators, name='dispatch')
class PrayerDeleteView(DeleteView):
    model = Prayer
    success_url = reverse_lazy('prayers:prayer_list')
