from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse

from weblog.models import Blog


class BlogViewTestCase(TestCase):
    def setUp(self):
        Blog(pk=1, name='Writing views', tagline='---')
        Blog.objects.create()

    def test_get_one_blog(self):
        client = Client()
        path = reverse('weblog:id-blog', kwargs={'id': 1, })
        resp = client.get(path)
        print(resp)

    def test_get_url(self):
        reverse('id-blog')

    def test_get_current_time(self):
        client = Client()
        path = reverse('weblog:current-time')
        resp = client.get(path)
        print(resp)


class CutomerErrorHandlerTests(SimpleTestCase):

    def test_handler_redeners_template_response(self):
        response = self.client.get('/404/')


class ResponseTestCase(TestCase):
    def test_1(self):
        pass
