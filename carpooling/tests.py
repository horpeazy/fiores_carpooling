from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.test.client import Client
from django.contrib.auth.decorators import login_required
from carpooling.models import Trip
import json


# Create your tests here.

class TripModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='testuser', password='testpass')
		self.trip = Trip.objects.create(
			user=self.user,
			driver='Test Driver',
			origin='Test Origin',
			destination='Test Destination',
			origin_lat='0.0',
			origin_lon='0.0',
			destination_lat='1.0',
			destination_lon='1.0',
			route='Test Route',
			role=Trip.DRIVER,
			status=Trip.ACTIVE,
		)
		
	def test_trip_creation(self):
		trip = Trip.objects.create(
			user=self.user,
			driver='Test Driver',
			origin='Test Origin',
			destination='Test Destination',
			origin_lat='0.0',
			origin_lon='0.0',
			destination_lat='1.0',
			destination_lon='1.0',
			route='Test Route',
			role=Trip.DRIVER,
			status=Trip.ACTIVE,
		)
		self.assertEqual('Test Driver', trip.driver)
		self.assertEqual(trip.user, self.user)
		
	def test_trip_driver_max_length(self):
		max_length = self.trip._meta.get_field('driver').max_length
		self.assertEquals(max_length, 255)
		
	def test_trip_role_choices(self):
		choices = [choice[0] for choice in self.trip._meta.get_field('role').choices]
		self.assertEquals(choices, ['driver', 'passenger'])
		
	def test_trip_status_choices(self):
		choices = [choice[0] for choice in self.trip._meta.get_field('status').choices]
		self.assertEquals(choices, ['active', 'ended'])
		
	def test_trip_default_status(self):
		trip = Trip.objects.create(
			user=self.user,
			driver='Test Driver',
			origin='Test Origin',
			destination='Test Destination',
			origin_lat='0.0',
			origin_lon='0.0',
			destination_lat='1.0',
			destination_lon='1.0',
			route='Test Route',
			role=Trip.DRIVER,
		)
		self.assertEqual(trip.status, Trip.ACTIVE)


class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')
        self.username = 'testuser'
        self.password = 'testpass123'

    def test_signup_view_form_valid(self):
        """
        Test that a user can sign up successfully with valid form data.
        """
        data = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
        user = User.objects.get(username=self.username)
        self.assertTrue(user.check_password(self.password))

    def test_signup_view_form_invalid(self):
        """
        Test that a user cannot sign up with invalid form data.
        """
        data = {
            'username': '',
            'password1': self.password,
            'password2': self.password
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_signup_view_template(self):
        """
        Test that the correct template is used to render the view.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_signup_view_form_class(self):
        """
        Test that the correct form class is used in the view.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserCreationForm)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.home_url = reverse('home_view')
        self.login_url = reverse('login')
        
    def test_home_view_with_authenticated_user(self):
        # Log in the user first
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.home_url)
        
        # Check that the response status code is 200 and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carpooling/index.html')
    
    def test_home_view_with_unauthenticated_user(self):
        response = self.client.get(self.home_url)
        
        # Check that the response status code is 302 (redirect) and the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.home_url}')
        
    def test_home_view_redirect_after_login(self):
        # Access the home page without being logged in
        response = self.client.get(self.home_url)
        
        # Check that the response status code is 302 (redirect) and the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        
        # Log in the user and check that they are redirected back to the home page
        login_response = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login_response)
        
        # Check that the response status code is 302 (redirect) and the user is redirected to the home page
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carpooling/index.html')
        

class JoinPoolViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('join_pool')
        
    def test_join_pool_view_authenticated_access(self):
        # Create a user and log them in
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Test that an authenticated user can access the view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carpooling/join_pool.html')
        
    def test_join_pool_view_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')
        
    def test_join_pool_view_redirect(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/join_pool/')


class CreatePoolViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_pool')
        
    def test_create_pool_view_authenticated_access(self):
        # Create a user and log them in
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Test that an authenticated user can access the view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carpooling/create_pool.html')
        
    def test_create_pool_view_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')
        
    def test_create_pool_view_redirect(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/create_pool/')
        

class TripsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('trips')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.trip = Trip.objects.create(
            user=self.user,
            driver='Test driver',
            origin='Test origin',
            destination='Test destination',
            origin_lat='0.0',
            origin_lon='0.0',
            destination_lat='0.0',
            destination_lon='0.0',
            route='Test route',
            role=Trip.DRIVER,
            status=Trip.ACTIVE
        )

    def test_trips_view_unauthenticated_access(self):
        # Test that an unauthenticated user is redirected to the login page
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')

    def test_trips_view_authenticated_access(self):
        # Test that an authenticated user can access the trips view
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carpooling/trips.html')
        self.assertContains(response, 'My Trips')
        self.assertContains(response, 'Test driver')
        self.assertContains(response, 'Test origin')
        self.assertContains(response, 'Test destination')

    def test_trips_view_returns_trips_for_authenticated_user(self):
        # Test that the trips view returns only the trips belonging to the authenticated user
        user2 = User.objects.create_user(username='testuser2', password='testpass')
        trip2 = Trip.objects.create(
            user=user2,
            driver='Test driver 2',
            origin='Test origin 2',
            destination='Test destination 2',
            origin_lat='1.0',
            origin_lon='1.0',
            destination_lat='1.0',
            destination_lon='1.0',
            route='Test route 2',
            role=Trip.PASSENGER,
            status=Trip.ACTIVE
        )
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['trips']), 1)
        self.assertEqual(response.context['trips'][0], self.trip)
        
        
class TripDetailTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='secret'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='secret2'
        )
        self.trip = Trip.objects.create(
            user=self.user,
            driver='John',
            origin='San Francisco',
            destination='Los Angeles',
            origin_lat='37.7749',
            origin_lon='-122.4194',
            destination_lat='34.0522',
            destination_lon='-118.2437',
            route='[[37.7749,-122.4194],[34.0522,-118.2437]]',
            role='driver',
            status='active'
        )
        self.url = reverse('trip_detail', args=[self.trip.id])

    def test_trip_detail_view_authenticated(self):
        self.client.login(username='testuser', password='secret')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carpooling/trip_detail.html')
        self.assertEqual(response.context['trip'], self.trip)
        self.assertListEqual(list(response.context['matches']), [])

    def test_trip_detail_view_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')

    def test_trip_detail_view_matches(self):
        self.client.login(username='testuser', password='secret')
        trip1 = Trip.objects.create(
            user=self.user2,
            driver='Sarah',
            origin='San Francisco',
            destination='Los Angeles',
            origin_lat='37.7749',
            origin_lon='-122.4194',
            destination_lat='34.0522',
            destination_lon='-118.2437',
            route='[[37.7749,-122.4194],[34.0522,-118.2437]]',
            role='passenger',
            status='active'
        )
        trip2 = Trip.objects.create(
            user=self.user2,
            driver='Bob',
            origin='San Francisco',
            destination='Los Angeles',
            origin_lat='37.7749',
            origin_lon='-122.4194',
            destination_lat='34.0522',
            destination_lon='-118.2437',
            route='[[37.7749,-122.4194],[34.0522,-118.2437]]',
            role='passenger',
            status='active'
        )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['matches']), 2)


class MatchDriverTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('match_driver')
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_match_driver_success(self):
        # Create an active driver trip
        driver_trip = Trip.objects.create(
            user=User.objects.create_user(username='driver'),
            destination='Destination',
            origin='Origin',
            role=Trip.DRIVER,
            status=Trip.ACTIVE,
            route=[[51.5074, 0.1278], [51.5080, 0.1279], [51.5082, 0.1280]]
        )

        # Send a matching request
        response = self.client.post(
            self.url,
            json.dumps({
                'route': [[51.5073, 0.1278], [51.5080, 0.1279], [51.5082, 0.1280], [51.5083, 0.1281]],
                'destination': 'Destination',
                'location': 'Origin',
                'origin_lat': 10.0,
                'origin_lon': 20.0,
                'destination_lat': 30.0,
                'destination_lon': 40.0,
            }),
            content_type='application/json'
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 1)
        self.assertEqual(response.json()['result'][0]['username'], 'driver')    

    def test_match_driver_inactive_trips(self):
        # Create an inactive driver trip
        driver_trip = Trip.objects.create(
            user=User.objects.create_user(username='driver'),
            destination='Destination',
            origin='Origin',
            role=Trip.DRIVER,
            status=Trip.INACTIVE,
            route=[[37.7749,-122.4194],[34.0522,-118.2437]]
        )

        # Send a matching request
        response = self.client.post(
            self.url,
            json.dumps({
                'route': [[37.7749,-122.4194],[34.0522,-118.2437]],
                'destination': 'Destination',
                'location': 'Origin',
                'origin_lat': 10.0,
                'origin_lon': 20.0,
                'destination_lat': 30.0,
                'destination_lon': 40.0,
            }),
            content_type='application/json'
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 0)

    def test_match_driver_no_match(self):
        # Create an active driver trip
        driver_trip = Trip.objects.create(
            user=User.objects.create_user(username='driver'),
            destination='Destination',
            origin='Another Origin',
            role=Trip.DRIVER,
            status=Trip.ACTIVE,
            route=[[37.7749,-122.4194],[34.0522,-118.2437]]
        )

        # Send a matching request
        response = self.client.post(
            self.url,
            json.dumps({
                'route': [[37.7749,-122.4194],[4.0522,-5.2437]],
                'destination': 'Destination',
                'location': 'Origin',
                'origin_lat': 10.0,
                'origin_lon': 20.0,
                'destination_lat': 30.0,
                'destination_lon': 40.0,
            }),
            content_type='application/json'
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 0)
        
    def test_match_driver_wrong_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["message"], "Method Not Allowed")
        
        
class MatchPassengerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('match_passenger')
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_match_passenger_success(self):
        # Create an active driver trip
        passenger_trip = Trip.objects.create(
            user=User.objects.create_user(username='passenger'),
            destination='Destination',
            origin='Origin',
            role=Trip.PASSENGER,
            status=Trip.ACTIVE,
            route=[[51.5073, 0.1278], [51.5080, 0.1279], [51.5082, 0.1280], [51.5083, 0.1281]]
        )

        # Send a matching request
        response = self.client.post(
            self.url,
            json.dumps({
                'route': [[51.5073, 0.1278], [51.5080, 0.1279], [51.5082, 0.1280]],
                'destination': 'Destination',
                'location': 'Origin',
                'origin_lat': 10.0,
                'origin_lon': 20.0,
                'destination_lat': 30.0,
                'destination_lon': 40.0,
            }),
            content_type='application/json'
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 1)
        self.assertEqual(response.json()['result'][0]['username'], 'passenger')    

    def test_match_passenger_inactive_trips(self):
        # Create an inactive driver trip
        passenger_trip = Trip.objects.create(
            user=User.objects.create_user(username='passenger'),
            destination='Destination',
            origin='Origin',
            role=Trip.PASSENGER,
            status=Trip.INACTIVE,
            route=[[37.7749,-122.4194],[34.0522,-118.2437]]
        )

        # Send a matching request
        response = self.client.post(
            self.url,
            json.dumps({
                'route': [[37.7749,-122.4194],[34.0522,-118.2437]],
                'destination': 'Destination',
                'location': 'Origin',
                'origin_lat': 10.0,
                'origin_lon': 20.0,
                'destination_lat': 30.0,
                'destination_lon': 40.0,
            }),
            content_type='application/json'
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 0)

    def test_passenger_driver_no_match(self):
        # Create an active driver trip
        passenger_trip = Trip.objects.create(
            user=User.objects.create_user(username='passenger'),
            destination='Destination',
            origin='Another Origin',
            role=Trip.DRIVER,
            status=Trip.ACTIVE,
            route=[[37.7749,-122.4194],[34.0522,-118.2437]]
        )

        # Send a matching request
        response = self.client.post(
            self.url,
            json.dumps({
                'route': [[37.7749,-122.4194],[4.0522,-5.2437]],
                'destination': 'Destination',
                'location': 'Origin',
                'origin_lat': 10.0,
                'origin_lon': 20.0,
                'destination_lat': 30.0,
                'destination_lon': 40.0,
            }),
            content_type='application/json'
        )

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 0)
        
    def test_match_passenger_wrong_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["message"], "Method Not Allowed")
