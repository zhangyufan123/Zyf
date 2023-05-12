"""cw2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from nnr_payment.views import signup, signin, statement, payment_information, payment_check, payment_order, \
    payment_return, Transfer, Balance, deposit
from nnr_payment import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Payment_nnr/signin/', signin),
    path('Payment_nnr/signup/', signup),
    path('Payment_nnr/statement/', statement),
    path('Payment_nnr/Payment_information/', payment_information),
    path('Payment_nnr/Payment_check/', payment_check),
    path('Payment_nnr/Payment_order/', payment_order),
    path('Payment_nnr/Payment_return/', payment_return),
    path('Payment_nnr/deposit/', deposit),
    path('Payment_nnr/transfer/', Transfer),
    path('Payment_nnr/balance/', Balance),
]
