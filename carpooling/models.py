from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trip(models.Model):
	DRIVER = 'driver'
	PASSENGER = 'passenger'
	ACTIVE = 'active'
	INACTIVE = 'inactive'
	
	ROLE_CHOICES = [
		(DRIVER, 'driver'),
		(PASSENGER, 'passenger')
	]
	
	STATUS_CHOICES = [
		(ACTIVE, 'active'),
		(INACTIVE, 'inactive')
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	driver = models.CharField(max_length=255, blank=True, null=True)
	origin = models.CharField(max_length=500, blank=True, null=True)
	destination = models.CharField(max_length=500, blank=True, null=True)
	route = models.TextField(blank=True, null=True)
	role = models.CharField(max_length=10, choices = ROLE_CHOICES, default="passenger")
	status = models.CharField(max_length=10, choices = STATUS_CHOICES, default="active")
