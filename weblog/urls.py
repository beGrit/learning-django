from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, register_converter, include

from . import views, converters

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.DayConverter, 'day')

app_name = 'weblog'

urlpatterns = [
    # Commons常规资源(错误页面,成功页面,获取当前系统时间)
    path('', views.HomeIndexView.as_view(), name='home-index'),
    path('current-time/', views.current_time, name='current-time'),

    # 博客资源
    path('blog/', include([
        path('id/<int:id>/', views.IdBlogDetailView.as_view(), name='id-blog'),
    ])),

    # 类别功能
    path('categories/', include([
        path('id/<int:id>/', views.IdCategoryView.as_view(), name='id-category'),
        path('name/<str:name>/', views.NameCategoryView.as_view(), name='name-category'),
    ])),

    # 归档功能
    path('archives/', include([
        path('', views.YearsArchiveView.as_view(), name='archives'),
        path('year/list/', views.YearsArchiveView.as_view(), name='years-archive'),
        path('day/list', views.DaysArchiveView.as_view(), name='days-archive'),
        path('month/list', views.MonthsArchiveView.as_view(), name='months-archive'),
        path('<int:year>/', views.YearArchiveView.as_view(), name='year-archive'),
        path('<int:year>/<int:month>', views.MonthArchiveView.as_view(), name='month-archive'),
        path('<int:year>/<int:month>/<int:day>', views.DayArchiveView.as_view(), name='day-archive'),
    ])),

    # 标签功能
    path('categories/', include([
        path('', views.CategoriesView.as_view(), name='categories'),
    ])),

    # 上传文件功能
    path('upload-file/', include([
        path('', views.upload_file, name='upload-file'),
        path('multiple/', views.upload_multiple_files, name='upload-multiple-files'),
    ])),

    # 权限认证
    path('your-name/', views.handler_your_name, name='your-name'),
    path('test_model_form/', views.test_model_form, name='test-model-form'),
    path('oauth/', include([
        path('callback/', views.oauth_callback, name='oauth-callback'),
    ])),
    path('login/', views.LoginView.as_view(), name='login'),

    # about-me 关于我页面
    path('about/me/', views.AboutMeView.as_view(), name='about-me'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'weblog.error_views.http400'
handler403 = 'weblog.error_views.http403'
handler404 = 'weblog.error_views.http404'
handler500 = 'weblog.error_views.http500'
