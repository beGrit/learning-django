from django.urls import path, register_converter, include

from . import views, converters

register_converter(converters.FourDigitYearConverter, 'yyyy')

app_name = 'weblog'

urlpatterns = [
    path('', views.HomeIndexView.as_view(), name='home-index'),
    path('200/', views.operate_success, name='200-success'),
    path('current-time/', views.current_time, name='current-time'),
    path('upload-file/', include([
        path('', views.upload_file, name='upload-file'),
        path('multiple/', views.upload_multiple_files, name='upload-multiple-files'),
    ])),
    path('blog/', include([
        path('id/<int:id>/', views.IdBlogDetailView.as_view(), name='id-blog'),
        path('year/<yyyy:year>/', views.year_blog),
    ])),
    path('categories/', include([
        path('id/<int:id>/', views.IdCategoryView.as_view(), name='id-category'),
        path('name/<str:name>/', views.NameCategoryView.as_view(), name='name-category'),
    ])),
    path('your-name/', views.handler_your_name, name='your-name'),
    path('test_model_form/', views.test_model_form, name='test-model-form'),
]
