from django.http import HttpResponse


def index(request):
    a = 1
    b = 2
    c = a + b
    return HttpResponse("Hello, world {0}.".format(c))


def as_breakpoint(request):
    breakpoint()
    return HttpResponse("Hello, world.")


def as_exception(request):
    raise Exception("Oh no!!")
    return HttpResponse("Hello, world.")