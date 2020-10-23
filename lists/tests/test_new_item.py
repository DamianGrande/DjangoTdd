from django.test import TestCase

from lists.models import List, Item


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'A new item for an existing list.'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list.')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item for an existing list.'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
