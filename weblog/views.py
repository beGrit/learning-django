import datetime

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from weblog.forms import UploadFileForm, ContactForm, UploadMultipleFilesForm, BlogForm, EntryForm
from weblog.models import Blog, Entry, Category, CategoryWidgetPage, RecentArticleWidgetPage
from weblog.utils import handle_uploaded_file


def current_time(request):
    now = datetime.datetime.now()
    html = '<html><body>It is now %s</body></html>' % now
    resp = HttpResponse()
    resp.write(html)
    return resp


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            logo = form.cleaned_data['logo']
            handle_uploaded_file(logo)
            url = reverse('weblog:200-success')
            return HttpResponseRedirect(url)
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        # 请求方式有问题,重新刷新页面给用户
        return render(request, 'upload.html', {'form': UploadFileForm()})


def upload_multiple_files(request):
    if request.method == 'POST':
        form = UploadMultipleFilesForm(request.POST, request.FILES)
        if form.is_valid():
            url = reverse('weblog:200-success')
            return HttpResponseRedirect(url)
    else:
        form = UploadMultipleFilesForm()
    return render(request, 'upload-multiple-files.html', context={'form': form})


def handler_your_name(request):
    if request.method == 'POST':
        # binding data to NameForm
        form = ContactForm(request.POST)
        # 提取数据并且构造邮件发送
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['1134187280@qq.com']
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message
                      , sender, recipients)
            path = reverse('weblog:200-success')
            return HttpResponseRedirect(path)
    else:
        form = ContactForm()
    return render(request, 'test_form.html', {'form': form})


class BlogListView(ListView):
    model = Blog

    def head(self, *args, **kwargs):
        last_blog = self.get_queryset()[:5]
        response = HttpResponse()
        response['Last-Blogs'] = last_blog
        return response


class BlogDetailView(View):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get(self, request, id):
        blog = get_object_or_404(Blog, pk=id)
        resp = TemplateResponse(request, 'blogs/index.html', context={'blog': blog})
        return resp

    def post(self, request):
        pass


def test_model_form(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.full_clean():
            return redirect('weblog:200-success')
    else:
        blog_form = BlogForm()
        entry_form = EntryForm()
    return render(request, 'tes_model_form.html',
                  context={
                      'blog_form': blog_form.as_table(),
                      'entry_form': entry_form.as_table(),
                  })


class HomeIndexView(View):
    http_method_names = ['get']

    def get(self, request):
        entries = get_list_or_404(Entry)[:5]
        widgets = []
        cw = CategoryWidgetPage()
        raw = RecentArticleWidgetPage()
        widgets.append(cw)
        widgets.append(raw)
        return render(request, 'home/index.html',
                      context={
                          'entries': entries,
                          'widgets': widgets,
                      })


class IdCategoryView(View):
    http_method_names = ['get']

    def get(self, request, id):
        category = get_object_or_404(Category, pk=id)
        entries = Entry.objects.filter(blog__category=category)
        return render(request, 'entries/index.html', context={
            'category': category,
            'entries': entries,
        })


class NameCategoryView(View):
    http_method_names = ['get']

    def get(self, request, name='django'):
        category = get_object_or_404(Category, name=name)
        entries = Entry.objects.filter(blog__category=category)
        return render(request, 'entries/index.html', context={
            'entries': entries,
        })


class IdBlogDetailView(View):
    http_method_names = ['get', 'post']

    def get(self, request, id):
        blog = get_object_or_404(Blog, pk=id)
        return render(request, 'blogs/index.html', context={'blog': blog})

    def post(self, request, id):
        return render(request, 'success_upload.html')


class CategoriesView(View):
    http_method_names = ['get']

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'categories/index.html', context={
            'categories': categories,
        })


def oauth_callback(request):
    print(request)


def login(request):
    from django.contrib.auth import authenticate, login
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        render(request, 'home/index.html')
    else:
        render(request, 'user/auth/login.html')


class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        return render(request, 'user/auth/login.html', )

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('weblog:home-index')
        else:
            # show the valid
            return render(request, 'user/auth/login.html')


class AboutMeView(View):
    http_method_names = ['get']

    def get(self, request):
        return render(request, 'common/about-me.html', )


'''
 Archive 归档区
'''


class YearsArchiveView(View):
    http_method_names = ['get']

    def get(self, request):
        context = {}
        keys = [2019, 2020, 2021]
        data = {}
        for key in keys:
            # 查询出来的数据按照发布时间排序,且限制最多10条
            qs = Blog.objects.filter(publish_time__year=key).order_by('publish_time__day')[0:3]
            count = Blog.objects.filter(publish_time__year=key).count()
            data[str(key)] = {}
            data[str(key)]['data'] = list(qs.values('id', 'title', 'publish_time'))
            data[str(key)]['totalCount'] = count
        context['code'] = 200
        context['data'] = data
        context['one'] = False
        return render(request, 'archives/YearArchives.html', context=context)


class YearArchiveView(View):
    http_method_names = ['get']

    def get(self, request, year):
        context = {}
        keys = [year]
        data = {}
        for key in keys:
            # 查询出来的数据按照发布时间排序,且限制最多10条
            qs = Blog.objects.filter(publish_time__year=key).order_by('publish_time__day')
            count = Blog.objects.filter(publish_time__year=key).count()
            data[str(key)] = {}
            data[str(key)]['data'] = list(qs.values('id', 'title', 'publish_time'))
            data[str(key)]['totalCount'] = count
        context['code'] = 200
        context['data'] = data
        context['one'] = True
        return render(request, 'archives/YearArchives.html', context=context)


class MonthArchiveView(View):
    pass


class MonthsArchiveView(View):
    pass


class DayArchiveView(View):
    def get(self, request, year, month, day):
        # 查询出来的数据按照发布时间排序,且限制最多10条
        query = Q(publish_time__year=year) & Q(publish_time__month=month) & Q(publish_time__day=day)
        qs = Blog.objects.filter(query).order_by('publish_time')
        count = Blog.objects.filter(query).count()

        if qs.count() == 0:
            raise Http404()

        # 构造data域
        data = {}
        key = str(year) + '/' + str(month) + '/' + str(day)
        data[key] = {}
        data[key]['data'] = list(qs.values('id', 'title', 'publish_time'))
        data[key]['totalCount'] = count
        data[key]['meta'] = {}
        data[key]['meta']['year'] = year
        data[key]['meta']['month'] = month
        data[key]['meta']['day'] = day

        context = {}
        context['code'] = 200
        context['data'] = data
        context['one'] = True
        return render(request, 'archives/DayArchives.html', context=context)

    def buildContext(self, key, data):
        pass

    def buildData(self, data, total_count):
        pass


class DaysArchiveView(View):
    pass
