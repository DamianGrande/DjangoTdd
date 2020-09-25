from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get(r'/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        self.client.post(r'/', data={'item_text': 'A new list item.'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item.')

    def test_redirects_after_POST(self):
        response = self.client.post(r'/', data={'item_text': 'A new list item.'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], r'/')

    def test_only_saves_item_when_necessary(self):
        self.client.get(r'/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get(r'/')

        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())
