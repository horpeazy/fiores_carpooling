from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trip(models.Model):
	DRIVER = 'driver'
	PASSENGER = 'passenger'
	ACTIVE = 'active'
	INACTIVE = 'ended'
	
	ROLE_CHOICES = [
		(DRIVER, 'driver'),
		(PASSENGER, 'passenger')
	]
	
	STATUS_CHOICES = [
		(ACTIVE, 'active'),
		(INACTIVE, 'ended')
	]

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	driver = models.CharField(max_length=255, blank=True, null=True)
	origin = models.CharField(max_length=500, blank=True, null=True)
	destination = models.CharField(max_length=500, blank=True, null=True)
	origin_lat = models.CharField(max_length=50, blank=True, null=True)
	origin_lon = models.CharField(max_length=50, blank=True, null=True)
	destination_lat = models.CharField(max_length=50, blank=True, null=True)
	destination_lon = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	route = models.TextField(blank=True, null=True)
	role = models.CharField(max_length=10, choices = ROLE_CHOICES)
	status = models.CharField(max_length=10, choices = STATUS_CHOICES, default="active")
	matches = models.TextField(blank=True, null=True)
