from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=30)
    profile_photo = models.ImageField(upload_to='weblog/static/images/avatars')
    register_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Author(User):
    # 博客发布数量
    publish_blog_count = models.IntegerField(default=0)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, models.CASCADE)
    publish_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('weblog:id-blog', args=[self.pk])

    def get_publish_date(self):
        return str(self.publish_time.date())

    def __str__(self):
        return self.title


class Entry(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.headline


class Category(models.Model):
    name = models.CharField(max_length=100)
    blog = models.ManyToManyField(Blog)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('weblog:id-category', args=[self.pk])

    def __str__(self):
        return self.name


class PageAbstractWidget(object):
    # 可注册的插件类型
    admit_name_space = ['分类', '原创图书', '最近的文章']

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # 创建的插件有误
        if value not in self.admit_name_space:
            raise Exception()
        self._name = value


class CategoryWidgetPage(PageAbstractWidget):
    def __init__(self):
        super(CategoryWidgetPage, self).__init__('分类')
        self._content = Category.objects.all()

    @property
    def content(self):
        return self._content


class RecentArticleWidgetPage(PageAbstractWidget):
    def __init__(self):
        super(RecentArticleWidgetPage, self).__init__('最近的文章')
        self._content = Blog.objects.order_by('publish_time')[:5]

    @property
    def content(self):
        return self._content
