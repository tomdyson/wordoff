from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.conf import settings
from wordoff import superClean

def index(request):
    return render_to_response('index.html', {})
    
def clean(request):
    input = request.POST["html"]
    cleaned = superClean(input)
    return render_to_response('cleaned.html', locals())