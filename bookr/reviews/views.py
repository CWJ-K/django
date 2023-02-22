#from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    name = request.GET.get('name') or 'world'
    #return HttpResponse('Hello, {}!'.format(name))
    return render(request, 'base.html', {'name': name})


def book_search(request):
    search_text = request.GET.get('search', '')
    return render(request, 'search-results.html', {'search_text': search_text})