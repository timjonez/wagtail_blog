from django.urls import path
from . import views

app_name = 'prayers'

urlpatterns = [
    path('', views.PrayerListView.as_view(), name='prayer_list'),
    path('prayer/<int:pk>', views.PrayerDetailView.as_view(), name='prayer_detail'),
    path('prayer/', views.CreatePrayerView.as_view(), name='create_prayer'),
    path('prayer/<int:pk>/edit/', views.PrayerUpdateView.as_view(), name='prayer_edit'),
    path('prayer/<int:pk>/remove/', views.PrayerDeleteView.as_view(), name='prayer_remove'),
]
