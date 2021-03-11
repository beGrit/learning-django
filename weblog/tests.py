from django.test import TestCase

from weblog.models import Blog


class BlogModelTests(TestCase):

    def test_create_one(self):
        # 使用 (keyword argument)
        b = Blog(name='aaa', tagline='bbb')
        b.save()

    def test_save_one(self):
        b = Blog.objects.get(pk=1)
        print(b)

    def test_get_one(self):
        query_set = Blog.objects.all()
        pk = 1
        try:
            query_set.get(pk=pk)
        except Blog.DoesNotExist:
            print('查找的记录不存在: pk=%d' % pk)
        except Blog.MultipleObjectsReturned:
            print('查找的结果有重复: pk=%d' % pk)
