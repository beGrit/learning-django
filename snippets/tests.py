from django.test import TestCase
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


# Create your tests here.
class MyTest(TestCase):
    def test_save_one_test(self):
        snippet = Snippet(code='foo = "bar\n"')
        snippet.save()

        snippet = Snippet(code='print("hello world")\n')
        snippet.save()

        serializer = SnippetSerializer(snippet)
        print(serializer.data)
