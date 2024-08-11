from django.shortcuts import render, get_object_or_404
from .models import Book, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm
from django.views.decorators.http import require_POST


@require_POST
def book_review(request, book_id):
    book = get_object_or_404(Book,
                             id=book_id
                             )
    review = None
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.save()
    return render(request, 'blog/books/review.html',
                                {'book': book,
                                        'form': form,
                                        'review': review})


def book_list(request):
    book_lists = Book.objects.all()
    paginator = Paginator(book_lists, 5)
    page_number = request.GET.get('page', 1)
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request,
    'blog/books/list.html',
        {'books': books})


def book_detail(request, year, month, day, slug):
    book = get_object_or_404(Book,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)
    reviews = book.reviews.all()
    form = ReviewForm()
    return render(request,
    'blog/books/detail.html',
        {'book': book,
                'reviews': reviews,
                'form': form})


