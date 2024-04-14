from django.urls import path 
from . import views 
urlpatterns=[
    path('currentData/', views.DivisaAPIView.as_view()),
    path('tableData/', views.TableData.as_view()),
    path('dataForex/', views.ForexSendDataView.as_view()),
     path('datagetForex/', views.ForexGETDataView.as_view()),
]