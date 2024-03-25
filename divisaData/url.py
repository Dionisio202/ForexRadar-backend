from django.urls import path 
from . import views 
urlpatterns=[
    path('currentData/', views.DivisaAPIViews.as_view()),
    path('tableData/', views.TableData.as_view()),
  
]