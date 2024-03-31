from django.urls import path 
from . import views 
urlpatterns=[
    path('currentData/', views.DivisaAPIView.as_view()),
    path('tableData/', views.TableData.as_view()),
    path('dataForex/', views.ForexDataView.as_view()),
     path('test/', views.SupabaseAuthView.as_view())
]