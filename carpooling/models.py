from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trip(models.Model):
	DRIVER = 'driver'
	PASSENGER = 'passenger'
	ACTIVE = 'started'
	INACTIVE = 'ended'
	PENDING = 'pending'
	
	ROLE_CHOICES = [
		(DRIVER, 'driver'),
		(PASSENGER, 'passenger')
	]
	
	STATUS_CHOICES = [
		(ACTIVE, 'started'),
		(PENDING, 'pending'),
		(INACTIVE, 'ended')
	]

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
	driver = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="driver_trip")
	passengers = models.ManyToManyField('self', blank=True, related_name='passenger_trips')
	requests = models.ManyToManyField('self', blank=True, related_name='requests')
	origin = models.CharField(max_length=500, blank=True, null=True)
	destination = models.CharField(max_length=500, blank=True, null=True)
	origin_lat = models.CharField(max_length=50, blank=True, null=True)
	origin_lon = models.CharField(max_length=50, blank=True, null=True)
	destination_lat = models.CharField(max_length=50, blank=True, null=True)
	destination_lon = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	route = models.TextField(blank=True, null=True)
	role = models.CharField(max_length=10, choices = ROLE_CHOICES)
	status = models.CharField(max_length=10, choices = STATUS_CHOICES, default="pending")
	

class Review(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_owner")
	reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
	trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip")
	review = models.TextField(blank=False, null=False)


class Vehicle(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicle_owner")
	model = models.CharField(max_length=50, blank=True, null=True)
	make = models.CharField(max_length=50, blank=False, null=False)
	plate_number = models.CharField(max_length=50, blank=False, null=False)
	driver_license = models.CharField(max_length=50, blank=False, null=False)
	color = models.CharField(max_length=50, blank=False, null=False)
	
