from django.urls import path 
from . import views 
urlpatterns=[
     path('register/', views.Register.as_view()),
     path('login/', views.Login.as_view()),
     path('getProfile/', views.getProfile.as_view()),
      path('updateProfileName/', views.UpdateProfileName.as_view()),
      path('changePassword/', views.changePassword.as_view())
]