from django.urls import path
from . import views

urlpatterns = [
    path('stream/', views.stream, name="stream"),
    path('service/', views.service, name="sevice"),
    path('caps/', views.caps, name="caps"),
    path('capture/', views.capture, name="capture"),
    path('classifier/', views.classifier, name="classifier"),
    path('check/', views.check, name="check"),
    path('purchase/', views.purchase, name="purchase"),
]