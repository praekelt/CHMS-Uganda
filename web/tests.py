# Tests
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class PageViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_indexpage_view(self):
        response = self.client.get(
            reverse('web.views.index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FamilyConnect")
