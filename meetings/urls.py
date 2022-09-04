from django.urls import path

from meetings import views

app_name = 'meetings'
urlpatterns = [
    # path('invite/', views.SendInvite.as_view(), name='invite'),  # Todo Fix missing template before enabling again
    # path('invite/success/', views.SendInviteSuccess.as_view(), name='invite-success'),
]
