from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Review
from .utils import average_rating
from django.shortcuts import render, get_object_or_404

from .models import Book, Review
from .utils import average_rating


def index(request):
    name = request.GET.get('name') or 'world'
    # return HttpResponse('Hello, {}!'.format(name))
    return render(request, 'base.html', {'name': name})


def book_search(request):
    search_text = request.GET.get('search', '')
    return render(request, 'search-results.html', {'search_text': search_text})


def welcome_view(request):
    # message = f'''<html><h1>Welcome to Bookr!</h1> \
    #         <p>{Book.objects.count()} books and counting!</p><html>
    #     '''
    # return HttpResponse(message)

    # render search TEMPLATES configurations for templates
    return render(request, 'base.html')


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append(
            {
                'book': book,
                'book_rating': book_rating,
                'number_of_reviews': number_of_reviews,
            }
        )
    context = {'book_list': book_list}
    return render(request, 'reviews/books_list.html', context)


def book_detail(request, pk):
    from loguru import logger

    book = get_object_or_404(Book, pk=pk)
    logger.warning('book', book)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {"book": book, "book_rating": book_rating, "reviews": reviews}
    else:
        context = {"book": book, "book_rating": None, "reviews": None}
    return render(request, "reviews/book_detail.html", context)
