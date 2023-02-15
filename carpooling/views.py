from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import ast
from .models import Trip
from .utils import match

# Create your views here.

class SignUpView(generic.CreateView):
	form_class = UserCreationForm
	success_url = '/login'
	template_name = 'registration/register.html'

def home_view(request):
	if request.user.is_authenticated:
		return render(request, "carpooling/index.html")
	else:
		return redirect("/login")
		
def join_pool(request):
	return render(request, "carpooling/join_pool.html")
	
def create_pool(request):
	return render(request, "carpooling/create_pool.html")
	
def trips(request):
	trips = Trip.objects.filter(user=request.user)
	return render(request, "carpooling/trips.html", {"trips": trips})
	
def trip_detail(request, trip_id):
	trip = Trip.objects.filter(user=request.user, id=trip_id).first()
	matches = []
	if trip.status == "active":
		if trip.role == "driver":
			trips = Trip.objects.filter(role=Trip.PASSENGER, status=Trip.ACTIVE)
		else:
			trips = Trip.objects.filter(role=Trip.DRIVER, status=Trip.ACTIVE)
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match(route, trip_route)
			if  match_rate >= 0.6:
				matches.append({
					'username': trip.user.username,
					'destination': trip.destination,
					'origin': trip.origin,
					'match_rate': match_rate * 100
				})
			
	return render(request, "carpooling/trip_detail.html", {"trip": trip, "matches": matches})

@csrf_exempt	
def match_driver(request):
	if request.method == "POST":
		request_body = json.loads(request.body)
		route = request_body.get("route")
		destination = request_body.get("destination")
		origin = request_body.get("location")
		origin_lat = request_body.get("origin_lat")
		origin_lon = request_body.get("origin_lon")
		destination_lat = request_body.get("destination_lat")
		destination_lon = request_body.get("destination_lon")
		# Cancel former trips and save the new trip
		trips = Trip.objects.filter(user=request.user, status=Trip.ACTIVE)
		for trip in trips:
			trip.status = Trip.INACTIVE
			trip.save()
		new_trip = Trip.objects.create(user=request.user, destination=destination,
					       route=route, role=Trip.PASSENGER, origin=origin,
					       origin_lat=origin_lat, origin_lon=origin_lon,
					       destination_lat=destination_lat, destination_lon=destination_lon)
		# find matches in the db
		trips = Trip.objects.filter(role=Trip.DRIVER, status=Trip.ACTIVE)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match(route, trip_route)
			if  match_rate >= 0.6:
				matches.append({
					'username': trip.user.username,
					'destination': trip.destination,
					'origin': trip.origin,
					'match_rate': match_rate * 100
				})
		return JsonResponse({"result": matches}, status=200)
	else:
		return JsonResponse({"message": "Method Not Allowed"}, status=405)
		
@csrf_exempt	
def match_passenger(request):
	if request.method == "POST":
		request_body = json.loads(request.body)
		route = request_body.get("route")
		destination = request_body.get("destination")
		origin = request_body.get("location")
		origin_lat = request_body.get("origin_lat")
		origin_lon = request_body.get("origin_lon")
		destination_lat = request_body.get("destination_lat")
		destination_lon = request_body.get("destination_lon")
		# Cancel former trips and save the new trip
		trips = Trip.objects.filter(user=request.user, status=Trip.ACTIVE)
		for trip in trips:
			trip.status = Trip.INACTIVE
			trip.save()
		new_trip = Trip.objects.create(user=request.user, destination=destination, origin=origin,
					       route=route, role=Trip.DRIVER, driver=request.user.username,
					       origin_lat=origin_lat, origin_lon=origin_lon,
					       destination_lat=destination_lat, destination_lon=destination_lon)
		# find matches in the db
		trips = Trip.objects.filter(role=Trip.PASSENGER, status=Trip.ACTIVE)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match(route, trip_route)
			if  match_rate >= 0.6:
				matches.append({
					'username': trip.user.username,
					'destination': trip.destination,
					'origin': trip.origin,
					'match_rate': match_rate * 100
				})
		return JsonResponse({"result": matches}, status=200)
	else:
		return JsonResponse({"message": "Method Not Allowed"}, status=405)
