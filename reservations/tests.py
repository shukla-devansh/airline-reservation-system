from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AdminDashboardAccessTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='customer', password='customer1234')
		self.admin_user = User.objects.create_superuser(
			username='adminuser',
			password='admin1234',
			email='admin@example.com'
		)

	def test_superuser_can_access_admin_dashboard(self):
		self.client.login(username='adminuser', password='admin1234')
		response = self.client.get(reverse('admin_dashboard'))
		self.assertEqual(response.status_code, 200)

	def test_non_superuser_cannot_access_admin_dashboard(self):
		self.client.login(username='customer', password='customer1234')
		response = self.client.get(reverse('admin_dashboard'))
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)

	def test_superuser_login_redirects_to_admin_dashboard(self):
		response = self.client.post(reverse('login'), {
			'username': 'adminuser',
			'password': 'admin1234',
		})
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('admin_dashboard'))
