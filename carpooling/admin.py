from django.contrib import admin
from .models import Trip, Review, Vehicle

# Register your models here.
admin.site.register(Trip)
admin.site.register(Review)
admin.site.register(Vehicle)
