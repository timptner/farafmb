from django.urls import path

from . import views

app_name = 'exams'
urlpatterns = [
    path('', views.InfoView.as_view(), name='info'),
    path('submit/', views.ExamSubmitView.as_view(), name='submit'),
    path('submit/done/', views.ExamSubmitDoneView.as_view(), name='submit_done'),
]
