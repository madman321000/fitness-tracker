from django.http import HttpResponse


def hello_world(request):
    """Return a plain Hello World response."""
    return HttpResponse("Hello, world!")

