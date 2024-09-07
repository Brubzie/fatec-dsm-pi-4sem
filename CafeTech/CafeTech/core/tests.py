from django.test import TestCase


class IndexViewTest(TestCase):
    def test_get_cadastro_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
