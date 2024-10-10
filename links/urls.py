from django.urls import path

from links import views

app_name = 'links'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('change_order/', views.change_order, name='change_order'),
    path('change_order/done/', views.ChangeOrderDoneView.as_view(), name='change_order_done'),
]
