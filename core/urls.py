from django.urls import path
from .views import contact_view, subscribe_newsletter, payment, sandra, payment_confirmation
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.packages, name='packages'),
    path('team/', views.team, name='team'),
    path('testimonials/', views.testimonial, name='testimonial'),
    path('contact/', contact_view, name='contact'),
    path('payment/', views.payment, name='payment'),
    path('payment/confirm/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('sandra/', views.sandra, name='sandra'),
]
