from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Vehicle


class SignupForm(UserCreationForm):
	model = forms.CharField(max_length=50)
	make = forms.CharField(max_length=50)
	plate_number = forms.CharField(max_length=50)
	driver_license = forms.CharField(max_length=50)
	color = forms.CharField(max_length=50)
	
	class Meta:
		model = User
		fields = [
			  "username", "email", "first_name", "last_name",
			  "password1", "password2", "model", "make",
			  "plate_number", "driver_license", "color",
			]
			
	def save(self, commit=True):
		user = super().save(commit=False)
		user.save()
		make = self.cleaned_data["make"]
		model = self.cleaned_data["model"]
		plate_number = self.cleaned_data["plate_number"]
		driver_license = self.cleaned_data["driver_license"]
		color = self.cleaned_data["color"]
		vehicle = Vehicle.objects.create(user=user, make=make,
						 model=model, plate_number=plate_number,
						 driver_license=driver_license, color=color)
		return user
