from django.conf.urls import url
from .views import signin, signup
from django.urls import path


urlpatterns = [path('signin/', signin),
    path('signup/', signup)

]