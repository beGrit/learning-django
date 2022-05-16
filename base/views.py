from django.views.generic import ListView


class CommonTableListView(ListView):
    paginate_by = 5

    def get_breadcrumb_name(self):
        pass

    def get_headers(self):
        pass

    def get_fields(self):
        pass

    def get_detail_route(self):
        pass
