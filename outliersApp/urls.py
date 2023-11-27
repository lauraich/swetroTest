from django.urls import path

from outliersApp import views

urlpatterns = [
    path('process_data',views.processData),
    path('check_patterns',views.checkPatterns)
]
