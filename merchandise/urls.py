from django.urls import path

from . import views

app_name = 'merchandise'
urlpatterns = [
    path('', views.OrderCreate.as_view(), name='create-order'),
    path('success/', views.OrderSuccess.as_view(), name='order-done'),
    path('verify/', views.verify_order, name='verify-order'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
]
