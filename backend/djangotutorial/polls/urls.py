from django.urls import path
from . import views
from .views import RegisterUser
urlpatterns = [ 
    path("api/register/", RegisterUser.as_view(),name='register'),
]