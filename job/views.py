from django.http import HttpResponse


def test(request):
    if request.method == 'POST':
        raw_data = request.body
        import json
        print(json.loads(raw_data, ))
    return HttpResponse()
