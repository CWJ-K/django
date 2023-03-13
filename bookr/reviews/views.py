from django.http import HttpResponse
from .utils import average_rating
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from .form import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from django.utils import timezone
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile


def index(request):
    # name = request.GET.get('name') or 'world'
    # return HttpResponse('Hello, {}!'.format(name))
    return render(request, 'base.html')  # , {'name': name})


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


def book_search(request):
    search_text = request.GET.get('search', '')
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data['search']:
        search = form.cleaned_data['search']
        search_in = form.cleaned_data.get('search_in') or 'title'
        if search_in == 'title':
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = \
                Contributor.objects.filter(first_names__icontains=search)

            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            lname_contributors = \
                Contributor.objects.filter(last_names__icontains=search)

            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)
    return render(request, 'reviews/search-results.html', {'form': form, 'search_text': search_text, 'books': books})


def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, 'Publisher \'{}\' was created.'.format(updated_publisher))
            else:
                messages.success(request, 'Publisher \'{}\' was updated.'.format(updated_publisher))

            return redirect('publisher_edit', updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, 'reviews/instance-form.html',
                  {'form': form, 'instance': publisher, 'model_type': 'Publisher'})


def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)  # since we need to set the book attribute
            updated_review.book = book
            if review is None:
                messages.success(request, 'Review for "{}" created.'.format(book))
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, 'Review for "{}" updated'.format(book))
            updated_review.save()

            return redirect('book_detail', book.pk)

    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/instance-form.html',
                  {'form': form, 'instance': review, 'model_type': 'Review', 'related_instance': book,
                   'related_model_type': 'Book'})


def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(False)
            cover = form.cleaned_data.get('cover')

            if cover and not hasattr(cover, "path"):
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)
            book.save()
            messages.success(request, 'Book "{}" was successfully updated.'.format(book))
            return redirect('book_detail', book.pk)
    else:
        form = BookMediaForm(instance=book)

    return render(request, 'reviews/instance-form.html',
                  {'instance': book, 'form': form, 'model_type': 'Book', 'is_file_upload': True})
