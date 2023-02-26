from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import ast
from .models import Trip
from .utils import match, match_routes

# Create your views here.


class SignUpView(generic.CreateView):
	form_class = UserCreationForm
	success_url = '/login/'
	template_name = 'registration/register.html'


@login_required
def home_view(request):
	return render(request, "carpooling/index.html")
		

@login_required		
def join_pool(request):
	return render(request, "carpooling/join_pool.html")
	

@login_required	
def create_pool(request):
	return render(request, "carpooling/create_pool.html")
	

@login_required	
def trips(request):
	trips = Trip.objects.filter(user=request.user)
	return render(request, "carpooling/trips.html", {"trips": trips[::-1]})
	

@login_required
def end_trip(request, trip_id):
	trip = Trip.objects.filter(user=request.user, id=trip_id).first()
	trip.status = Trip.INACTIVE
	trip.save()
	return redirect("home_view")
	

@login_required
def trip_detail(request, trip_id):
	trip = Trip.objects.filter(user=request.user, id=trip_id).first()
	matched = []    # matched result
	matches = []    # possible matches
	if trip.role == "passenger":
		trips = Trip.objects.filter(role=Trip.DRIVER, status=Trip.ACTIVE).\
						   exclude(Q(user=request.user))
		if trip.matches:
			match_id = ast.literal(trip.matches)[0]
			match = Trip.objects.filter(id=match_id).first()
			matched.append(match)
		if trip.status == "active":
			for mtrip in trips:
				# Convert the route string to a list of coordinates.
				trip_route = ast.literal_eval(mtrip.route)
				match_rate = match(ast.literal_eval(trip.route), trip_route)
				if match_rate >= 0.4 and mtrip not in matched:
					mtrip.match_rate = match_rate * 100
					matches.append(mtrip)
	else:
		trips = Trip.objects.filter(role=Trip.PASSENGER, status=Trip.ACTIVE).\
						    exclude(Q(user=request.user))
		if trip.matches:
			match_ids =  ast.literal(trip.matches)
			for match_id in match_ids:
				match = Trip.objects.filter(id=match_id).first()
				matched.append(match)
		if trip.status:
			for mtrip in trips:
				# Convert the route string to a list of coordinates.
				trip_route = ast.literal_eval(mtrip.route)
				match_rate = match(ast.literal_eval(trip.route), trip_route)
				if match_rate >= 0.4 and mtrip not in matched:
					mtrip.match_rate = match_rate * 100
					matches.append(mtrip)
	context = {
		"trip": trip,
		"matched": matched,
		"matches": matches
	}
	return render(request, "carpooling/trip_detail.html", {"context": context})


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
					       destination_lat=destination_lat,
					       destination_lon=destination_lon)
		# find matches in the db
		trips = Trip.objects.filter(role=Trip.DRIVER, status=Trip.ACTIVE)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match_routes(route, trip_route)
			if  match_rate >= 0.4:
				matches.append({
					'match_id': trip.id,
					'username': trip.user.username,
					'destination': trip.destination,
					'origin': trip.origin,
					'origin_lon': trip.origin_lon,
					'origin_lat': trip.origin_lat,
					'match_rate': match_rate * 100
				})
		return JsonResponse({"result": matches, 'id': new_trip.id}, status=200)
	else:
		trip_id = request.GET.get("trip_id", None)
		match_id = request.GET.get("match_id", None)
		trip = Trip.objects.filter(id=trip_id).first()
		match = Trip.objects.filter(id=match_id).first()
		matches = ast.literal_eval(match.matches)
		if matches:
			matches.append(trip_id)
		else:
			matches = [trip_id]
		trip.matches = [match_id]
		match.matches = matches
		return redirect(trip_detail, trip_id=trip_id)
		
		
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
					       destination_lat=destination_lat, 
					       destination_lon=destination_lon)
		# find matches in the db
		trips = Trip.objects.filter(role=Trip.PASSENGER, status=Trip.ACTIVE)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match(route, trip_route)
			if  match_rate >= 0.4:
				matches.append({
					'username': trip.user.username,
					'destination': trip.destination,
					'origin': trip.origin,
					'origin_lon': trip.origin_lon,
					'origin_lat': trip.origin_lat,
					'match_rate': match_rate * 100
				})
		return JsonResponse({"result": matches, 'id': new_trip.id}, status=200)
	else:
		trip_id = request.args.GET("trip_id", None)
		match_id = request.args.GET("match_id", None)
		trip = Trip.objects.filter(id=trip_id).first()
		match = Trip.objects.filter(id=match_id).first()
		matches = ast.literal_eval(trip.matches)
		if matches:
			matches.append(match_id)
		else:
			matches = [match_id]
		trip.matches = matches
		match.matches = [trip_id]
		return redirect(trip_detail, trip_id=trip_id)
