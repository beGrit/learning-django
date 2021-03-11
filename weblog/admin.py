from django.contrib import admin
from weblog.models import *

admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Entry)
