from django.test import Client, TestCase


class TestView(TestCase):
    def test_get_one_animal(self):
        c = Client()
        resp = c.get('/testing/animal/', data={'id': 1})
        print(resp.status_code)
