from django.http import HttpResponse


def health_check(_request):
    response = HttpResponse("ok", content_type="text/plain")
    response["Cache-Control"] = "no-store"
    return response
