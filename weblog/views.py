import datetime

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.template import Context
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView

from weblog.forms import UploadFileForm, ContactForm, UploadMultipleFilesForm, BlogForm, EntryForm
from weblog.models import Blog, Entry, Category, CategoryWidget, RecentArticleWidget
from weblog.utils import handle_uploaded_file


def get_one_blog(request, id):
    pass


def year_blog(request, year):
    pass


def current_time(request):
    now = datetime.datetime.now()
    html = '<html><body>It is now %s</body></html>' % now
    resp = HttpResponse()
    resp.write(html)
    print(resp.content)
    print(resp.getvalue())
    return resp


def my_custom_page_not_found_view(request):
    return HttpResponse('404 not found')


def page_not_found_view(request):
    return render(request, '404.html')


def operate_success(request):
    return render(request, '200.html')


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
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


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


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_blogs'] = Blog.objects.all()[:5]
        return context


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
        resp = TemplateResponse(request, 'blog_detail/index.html', context={'blog': blog})
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
        cw = CategoryWidget()
        raw = RecentArticleWidget()
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
        context = Context()
        return render(request, 'blog_detail/index.html', context={'blog': blog})

    def post(self, request, id):
        return render(request, 'success_upload.html')


class CategoriesView(View):
    http_method_names = ['get']

    def get(self, request):
        categories = Category.objects.all()
        return render(request, '', context={
            'categories': categories,
        })


class ArchivesView(View):
    http_method_names = ['get']

    def get(self, request):
        context = Context()
        keys = [2019, 2020, 2021]
        context['years'] = []
        '''
            'years':{
                '2019':[
                    {},
                    {},
                    {},
                ],
                '2020':[
                ],
                '2021':[
                ]
            }
        '''
        data = {}
        for key in keys:
            qs = Blog.objects.filter(publish_time__year=key).order_by('publish_time__day')
            data[str(key)] = qs.values('id', 'title', 'publish_time')
        context['years'] = data
        return render(request, 'archives/index.html', context=context.dicts[0])


class YearArchivesView(View):
    http_method_names = ['get']

    def get(self, request, year):
        blogs = Blog.objects.filter(publish_time__year=year)
        return render(request, '', context={
            'year': year,
            'blogs': blogs,
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
        render(request, 'login.html')


class LoginView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        return render(request, 'login.html', )

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('weblog:home-index')
        else:
            # show the valid
            return render(request, 'login.html')
