from html import escape

from django.test import TestCase

from lists.models import Item, List


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new/', data={'item_text': 'A new list item.'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item.')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new/', data={'item_text': 'A new list item.'})
        self.assertRedirects(response, f'/lists/{List.objects.first().id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')
        expected_error = escape("You can't have an empty list item.")
        self.assertContains(response, expected_error)
