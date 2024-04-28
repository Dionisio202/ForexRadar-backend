from django.urls import path 
from . import views 
urlpatterns=[
    path('currentData/', views.DivisaAPIView.as_view()),
    path('tableData/', views.TableData.as_view()),
    path('dataForex/', views.ForexSendDataView.as_view()),
     path('datagetForex/', views.ForexGETDataView.as_view()),
      path('divisaInformation/', views.DivisasInformation.as_view()),
    path('insertarDivisaInformation/', views.InsertarDivisasUser.as_view()),
      path('obtenerDivisas/', views.DivisasOwn.as_view()), #solucionar  con referencias de tablas de supabase 
      path('eliminarDivisas/', views.divisasDeleteInformation.as_view()),
      path('dataForexApi/', views.ForexDataView.as_view()),
      path('dataprueba/', views.ForexGETDataSelectView.as_view()),
]