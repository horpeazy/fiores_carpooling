import json
import ast
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from .forms import SignupForm
from .models import Trip, Review, Vehicle
from .utils import match, match_routes


# Get current user model
#User = get_user_model()


# Create your views here.

def signup_view(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect('home_view')
		messages.error(request, "Invalid form")
		print(form.errors)
	else:
		form = SignupForm()
	return render(request, 'registration/register.html' ,{'form': form})

	
def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect("home_view")
			else:
				messages.error(request, "Invalid username or password")
	else:
		form = AuthenticationForm()
	return render(request, "registration/login.html", {"form": form})


def logout_view(request):
	logout(request)
	return redirect('login_view')

@login_required
def home_view(request):
	return render(request, "carpooling/index.html")
	
def map_view(request):
	return render(request, "carpooling/map.html")
	
@login_required
def account(request):
	user = request.user
	vehicle = Vehicle.objects.filter(user=request.user).first()
	context = {
		"user": user,
		"vehicle": vehicle,
	}
	return render(request, "carpooling/account.html", {"context": context})
	
@login_required
def profile(request, user_id):
	user = User.objects.filter(id=user_id).first()
	vehicle = Vehicle.objects.filter(user=user).first()
	context = {
		"user": user,
		"vehicle": vehicle,
	}
	return render(request, "carpooling/profile.html", {"context": context})
		

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
def end_trip(request):
	if request.method == "POST":
		trip_id = request.POST.get("trip_id")
		user_id = request.POST.get("user_id")
		review = request.POST.get("review")
		trip = Trip.objects.filter(user=request.user, id=trip_id).first()
		user = User.objects.filter(id=user_id).first()
		if review:
			review = Review.objects.create(user=user, review=review,
						       reviewer=request.user, trip=trip)
	else:
		trip_id = request.GET.get("trip_id")
		trip = Trip.objects.filter(user=request.user, id=trip_id).first()
	trip.status = Trip.INACTIVE
	trip.save()
	return redirect("trip_detail", trip_id)
	

@login_required
@csrf_exempt
def create_review(request):
	if request.method == "POST":
		request_body = json.loads(request.body)
		review = request_body.get("review")
		user_id = request_body.get("user_id")
		trip_id = request_body.get("trip_id")
		trip = Trip.objects.filter(id=trip_id).first()
		user = User.objects.filter(id=user_id).first()
		if review:
			review = Review.objects.create(user=user, review=review,
						       reviewer=request.user, trip=trip)
		response = {
			"message": 'Created Successfully'
		}
		return JsonResponse(response, status=201)
	

@login_required
def trip_detail(request, trip_id):
	trip = Trip.objects.filter(user=request.user, id=trip_id).first()
	matches = []    # possible matches
	if trip.role == "passenger":	
		if trip.status == Trip.ACTIVE:
			trips = Trip.objects.filter(role=Trip.DRIVER).\
				     exclude(Q(user=request.user)).\
				     exclude(Q(status=Trip.INACTIVE))
			for mtrip in trips:
				# Convert the route string to a list of coordinates.
				trip_route = ast.literal_eval(mtrip.route)
				match_rate = match_routes(ast.literal_eval(trip.route), trip_route)
				# add the match to potential matches if it's not the driver
				if match_rate >= 0.4 and mtrip.user != trip.driver:
					mtrip.match_rate = match_rate * 100
					matches.append(vars(mtrip))
	else:	
		if trip.status == Trip.ACTIVE:
			trips = Trip.objects.filter(role=Trip.PASSENGER, status=Trip.PENDING).\
						    exclude(Q(user=request.user))
			for mtrip in trips:
				# Convert the route string to a list of coordinates.
				trip_route = ast.literal_eval(mtrip.route)
				match_rate = match_routes(ast.literal_eval(trip.route), trip_route)
				review = Review.objects.filter(reviewer=mtrip.user, trip=trip).first()
				print(review)
				if ( match_rate >= 0.4 and mtrip not in trip.passengers
				     and mtrip not in trip.requests ):
					mtrip.match_rate = match_rate * 100
					mtrip = vars(mtrip)
					matches.append(vars(mtrip))
	requests = trip.requests.all()
	passengers = trip.passengers.all()
	driver = trip.driver
	trip =  vars(trip)
	trip["requests"] = requests
	trip["passengers"] = passengers
	trip["driver"] = driver
	context = {
		"trip": trip,
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
		trips = Trip.objects.filter(user=request.user).exclude(Q(status=Trip.INACTIVE))
		for trip in trips:
			trip.status = Trip.INACTIVE
			trip.save()
		new_trip = Trip.objects.create(user=request.user, destination=destination,
					       route=route, role=Trip.PASSENGER, origin=origin,
					       origin_lat=origin_lat, origin_lon=origin_lon,
					       destination_lat=destination_lat,
					       destination_lon=destination_lon)
		# find matches in the db
		trips = Trip.objects.filter(role=Trip.DRIVER).exclude(Q(status=Trip.INACTIVE))
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match_routes(route, trip_route)
			if  match_rate >= 0.4:
				matches.append({
					'id': trip.id,
					'username': trip.user.username,
					'user_id': trip.user.id,
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
		if trip and match:
			# trip.requests.add(match)
			match.requests.add(trip)
			trip.save()
			match.save()
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
		trips = Trip.objects.filter(user=request.user).exclude(Q(status=Trip.INACTIVE))
		for trip in trips:
			trip.status = Trip.INACTIVE
			trip.save()
		new_trip = Trip.objects.create(user=request.user, destination=destination, origin=origin,
					       route=route, role=Trip.DRIVER,
					       origin_lat=origin_lat, origin_lon=origin_lon,
					       destination_lat=destination_lat, 
					       destination_lon=destination_lon)
		# set the trip as the drivers trip
		new_trip.driver = new_trip
		new_trip.save()

		# find matches in the db
		trips = Trip.objects.filter(role=Trip.PASSENGER, status=Trip.PENDING)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match_routes(route, trip_route)
			if  match_rate >= 0.4:
				matches.append({
					'id': trip.id,
					'username': trip.user.username,
					'user_id': trip.user.id,
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
		if trip and match:
			# trip.requests.add(match)
			match.requests.add(trip)
			trip.save()
			match.save()
		return redirect(trip_detail, trip_id=trip_id)


@login_required
def accept_trip(request):
	trip_id = request.GET.get("ride_id", None)
	match_id = request.GET.get("match_id", None)
	trip = Trip.objects.filter(id=trip_id).first()
	match = Trip.objects.filter(id=match_id).first()
	
	if not trip or not match:
		return "oops"
	if trip.role == "passenger":
		trip.status = Trip.ACTIVE
		match.status = Trip.ACTIVE
		trip.driver = match
		trip.requests.remove(match)
		match.passengers.add(trip)
	else:
		trip.status = Trip.ACTIVE
		match.status = Trip.ACTIVE
		trip.passengers.add(match)
		trip.requests.remove(match)
		match.driver = trip
		
	trip.save()
	match.save()
	return redirect(trip_detail, trip_id=trip_id)
	

@login_required
def reviews(request):
	user_id = request.GET.get("user_id", None)
	if user_id:
		user = User.objects.filter(id=user_id).first()
	else:
		user = request.user
	reviews = Review.objects.filter(user=user).all()
	context = {
		"reviews": reviews,
	}
	return render(request, "carpooling/reviews.html", {"context": context})
