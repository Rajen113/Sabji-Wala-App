from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import LocationLog
from .utils import haversine

User = get_user_model()

class MapsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a customer user with location
        self.customer = User.objects.create_user(
            email='customer@example.com',
            full_name='Customer User',
            phone='1234567890',
            password='password123',
            user_type='customer',
            latitude=28.6139,  # Delhi coordinates
            longitude=77.2090
        )
        # Create seller users within 1 km
        self.seller1 = User.objects.create_user(
            email='seller1@example.com',
            full_name='Seller One',
            phone='1234567891',
            password='password123',
            user_type='seller',
            latitude=28.6140,  # Close to customer
            longitude=77.2091
        )
        self.seller2 = User.objects.create_user(
            email='seller2@example.com',
            full_name='Seller Two',
            phone='1234567892',
            password='password123',
            user_type='seller',
            latitude=28.6300,  # Farther, about 1.8 km
            longitude=77.2150
        )

    def test_nearby_sellers_map_view(self):
        self.client.login(email='customer@example.com', password='password123')
        response = self.client.get(reverse('nearby_sellers_map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'maps/nearby_map.html')
        # Check if seller1 is in context (within 1 km)
        sellers = response.context['sellers']
        self.assertEqual(len(sellers), 1)
        self.assertEqual(sellers[0]['name'], 'Seller One')
        # Check distance calculation
        distance = haversine(self.customer.latitude, self.customer.longitude, self.seller1.latitude, self.seller1.longitude)
        self.assertLessEqual(distance, 1)

    def test_update_location_view(self):
        self.client.login(email='customer@example.com', password='password123')
        response = self.client.post(reverse('update_location'), {
            'latitude': 28.7041,
            'longitude': 77.1025
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.latitude, 28.7041)
        self.assertEqual(self.customer.longitude, 77.1025)
