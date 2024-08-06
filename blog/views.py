from django.shortcuts import render, get_object_or_404
from .models import Book
from django.core.paginator import Paginator


def book_list(request):
    book_lists = Book.objects.all()
    paginator = Paginator(book_lists, 5)
    page_number = request.GET.get('page', 1)
    books = paginator.page(page_number)
    return render(request, 'blog/books/list.html', {'books': books})


def book_detail(request, year, month, day, slug):
    book = get_object_or_404(Book, publish__year=year, publish__month=month, publish__day=day, slug=slug)
    return render(request, 'blog/books/detail.html', {'book': book})


