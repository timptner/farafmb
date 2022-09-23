from django.urls import path

from . import views

app_name = 'merchandise'
urlpatterns = [
    path('', views.OrderCreateView.as_view(), name='order-create'),
    path('success/', views.OrderSuccessView.as_view(), name='order-done'),
    path('verify/', views.verify_order, name='order-verify'),
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
]
