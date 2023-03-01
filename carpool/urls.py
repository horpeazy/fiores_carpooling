"""carpool URL Configuration

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
from carpooling.views import ( home_view, SignUpView, 
			       join_pool, match_driver, 
			       match_passenger, trips, 
			       create_pool, trip_detail,
			       end_trip, accept_trip
			     )

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_view, name="home_view"),
    path("", include("django.contrib.auth.urls")),
    path("register/", SignUpView.as_view(), name='signup'),
    path("join-ride/", join_pool, name="join_pool"),
    path("create-ride/", create_pool, name="create_pool"),
    path("match/driver/", match_driver, name="match_driver"),
    path("match/passenger/", match_passenger, name="match_passenger"),
    path("trips/", trips, name="trips"),
    path("trips/<int:trip_id>/", trip_detail, name="trip_detail"),
    path("end-trip/<int:trip_id>/", end_trip, name="end_trip"),
    path("accept-trip/", accept_trip, name="accept_trip"),
]
