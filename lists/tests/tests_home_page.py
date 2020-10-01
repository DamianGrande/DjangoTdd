from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(r'/')
        self.assertTemplateUsed(response, 'lists/home.html')
