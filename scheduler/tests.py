from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from scheduler.models import Product, Appointment, Order, OrderItem
import datetime

class HairGlowModelTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        
        # Create a test product
        self.product = Product.objects.create(
            name='Test Shampoo',
            description='A premium testing shampoo.',
            price=15.99,
            stock=10,
            image_path='images/test.png'
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Shampoo')

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            user=self.user,
            name='Test Customer',
            email='customer@example.com',
            phone='12345678',
            date=datetime.date.today(),
            time_slot='09:00 - 10:00',
            service_type='Hair Consultation'
        )
        self.assertEqual(appointment.status, 'Pending')
        self.assertEqual(str(appointment), f"Test Customer - {datetime.date.today()} @ 09:00 - 10:00 (Hair Consultation)")


class HairGlowViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123', email='tester@example.com')
        self.product = Product.objects.create(
            name='Luxury Oil',
            description='Restorative oil.',
            price=25.00,
            stock=5
        )

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_products_list_loads(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')
        self.assertContains(response, 'Luxury Oil')

    def test_booking_requires_login(self):
        response = self.client.get(reverse('book_appointment'))
        # Should redirect to login since LOGIN_URL = 'login'
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_booking_flow(self):
        self.client.login(username='tester', password='password123')
        
        # Test GET loads successfully
        response = self.client.get(reverse('book_appointment'))
        self.assertEqual(response.status_code, 200)
        
        # Test POST booking creation
        date_str = datetime.date.today().strftime('%Y-%m-%d')
        post_data = {
            'name': 'Tester Name',
            'email': 'tester@example.com',
            'phone': '987654321',
            'date': date_str,
            'time_slot': '10:00 - 11:00',
            'service_type': 'Scalp Analysis',
            'notes': 'Looking forward to it!'
        }
        
        response = self.client.post(reverse('book_appointment'), post_data)
        # Should redirect to dashboard on success
        self.assertRedirects(response, reverse('dashboard'))
        
        # Check database
        self.assertEqual(Appointment.objects.count(), 1)
        appt = Appointment.objects.first()
        self.assertEqual(appt.user, self.user)
        self.assertEqual(appt.time_slot, '10:00 - 11:00')

    def test_double_booking_prevention(self):
        self.client.login(username='tester', password='password123')
        
        date = datetime.date.today()
        # Create first booking directly
        Appointment.objects.create(
            user=self.user,
            name='Client A',
            email='a@example.com',
            phone='11111',
            date=date,
            time_slot='10:00 - 11:00',
            status='Pending'
        )
        
        # Try booking same slot via POST
        post_data = {
            'name': 'Client B',
            'email': 'b@example.com',
            'phone': '22222',
            'date': date.strftime('%Y-%m-%d'),
            'time_slot': '10:00 - 11:00',
            'service_type': 'Hair Consultation'
        }
        
        response = self.client.post(reverse('book_appointment'), post_data)
        # Should redirect back to booking page (with error) rather than dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_appointment'))
        
        # Booking count should still be 1 (second booking blocked)
        self.assertEqual(Appointment.objects.count(), 1)
