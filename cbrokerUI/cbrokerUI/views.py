from django.http import HttpResponse



def index(request):
    
    return HttpResponse("Hello World. You are at the index page.")