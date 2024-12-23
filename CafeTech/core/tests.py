from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class IndexViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_view_contains_user(self):
        User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")


class RegisterViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_view_can_register_user(self):
        form_data = {
            "username": "newuser",
            "password": "password123",
            "confirm_password": "password123",
            "phone_number": "1234567890",  # Adicionando o campo phone_number
        }
        response = self.client.post(reverse("register"), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_view_can_login_user(self):
        form_data = {"username": "testuser", "password": "12345"}
        response = self.client.post(reverse("login"), data=form_data)
        self.assertRedirects(response, reverse("index"))

    def test_view_login_with_incorrect_credentials(self):
        form_data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(reverse("login"), data=form_data)
        self.assertEqual(
            response.status_code, 200
        )  # Deveria retornar à mesma página com erro
        self.assertContains(
            response, "Credenciais incorretas"
        )  # Verifica a mensagem de erro, se disponível


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_to_login(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
