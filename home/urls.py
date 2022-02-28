from django.urls import path
from . import views
from django.contrib import admin

app_name = "home"


urlpatterns = [
    path('',views.home,name='index'),
    path('Done',views.Done,name='index'),
    path('scan/<slug:type>/',views.scan,name='scan'),
    path('PDF/<slug:type>/',views.ToPDF,name='scan'),
]