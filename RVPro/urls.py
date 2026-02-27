"""
URL configuration for RVPro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from RVApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index_page),
    path("index_page",views.index_page),
    path("login_register_page", views.login_register_page),
    path("fetchregister", views.fetchregister),
    path("login", views.login),
    path("logout", views.logout),
    path("car_list_page", views.car_list_page),
    path("add_car_page", views.add_car_page),
    path("fetchvehicledata", views.fetchvehicledata),
    path("contact_page", views.contact_page),
    path("fetchcontactdata", views.fetchcontactdata),
    path("maintain_page", views.maintain_page),
    path("fetchmaintanancedata", views.fetchmaintanancedata),
    path("single_car/<int:id>", views.single_car,name="single_car"),
    path("review", views.review),
    path("fetchreview", views.fetchreview),
    path("cargallery", views.cargallery),
    path("fetchgallery", views.fetchgallery),
    path("fetchgallarydata", views.fetchgallarydata),
    path("booking/<int:bookid>", views.booking),
    path("book_car", views.book_car_view, name="book_car"),
    path("my-bookings", views.my_bookings_view, name="my_bookings"),
    path("payment-success", views.payment_success, name="payment_success"),
    path('review/<int:booking_id>/', views.leave_review, name='leave_review'),
    path('eset_password', views.reset_password, name='reset_password'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
