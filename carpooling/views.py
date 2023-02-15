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

@csrf_exempt	
def match_driver(request):
	if request.method == "POST":
		request_body = json.loads(request.body)
		route = request_body.get("route")
		destination = request_body.get("destination")
		origin = request_body.get("location")
		# Cancel former trips and save the new trip
		trips = Trip.objects.filter(user=request.user, status=Trip.ACTIVE)
		for trip in trips:
			trip.status = Trip.INACTIVE
			trip.save()
		new_trip = Trip.objects.create(user=request.user, destination=destination,
					       route=route, role=Trip.PASSENGER, origin=origin)
		# find matches in the db
		trips = Trip.objects.filter(role=Trip.DRIVER, status=Trip.ACTIVE)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match(route, trip_route)
			print(match_rate)
			if  match_rate >= 0.6:
				matches.append({
					'username': trip.user.username,
					'destination': trip.destination,
					'match_rate': match_rate
				})
		print(matches)
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
		# Cancel former trips and save the new trip
		trips = Trip.objects.filter(user=request.user, status=Trip.ACTIVE)
		for trip in trips:
			trip.status = Trip.INACTIVE
			trip.save()
		new_trip = Trip.objects.create(user=request.user, destination=destination, origin=origin,
					       route=route, role=Trip.DRIVER, driver=request.user.username)
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
					'match_rate': match_rate
				})
		print(matches)
		return JsonResponse({"result": matches}, status=200)
	else:
		return JsonResponse({"message": "Method Not Allowed"}, status=405)
