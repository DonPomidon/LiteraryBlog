from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from .models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm, AddBookForm, BookFilterForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def blog_about(request):
    return render(request, 'blog/books/about.html')


def blog_contacts(request):
    return render(request, 'blog/books/contacts.html')


@require_POST
@login_required()
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

    return render(request, 'blog/books/review.html', {'book': book, 'form': form, 'review': review})


def book_list(request):
    book_lists = Book.objects.all()
    form = BookFilterForm(request.GET or None)

    if form.is_valid():
        author = form.cleaned_data.get('author')
        category = form.cleaned_data.get('category')
        min_rating = form.cleaned_data.get('min_rating')
        max_rating = form.cleaned_data.get('max_rating')

        if author:
            book_lists = book_lists.filter(author=author)
        if category:
            book_lists = book_lists.filter(category=category)
        if min_rating is not None:
            book_lists = book_lists.filter(rating__gte=min_rating)
        if max_rating is not None:
            book_lists = book_lists.filter(rating__lte=max_rating)

    paginator = Paginator(book_lists, 3)
    page_number = request.GET.get('page', 1)

    try:
        books = paginator.page(page_number)

    except PageNotAnInteger:
        books = paginator.page(1)

    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request,'blog/books/list.html', {'books': books, 'form': form})


def book_detail(request, year, month, day, slug):
    book = get_object_or_404(Book,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug)
    reviews = book.reviews.all()
    form = ReviewForm()

    return render(request,'blog/books/detail.html', {'book': book, 'reviews': reviews, 'form': form})


@login_required()
def book_add(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)

        if form.is_valid():
            book = form.save(commit=False)

            if not book.slug:
                book.slug = slugify(book.title)
            book.added_by = request.user
            book.save()
            return redirect('blog:book_list')
        else:
            form.add_error(None, 'Wrong data!')
    else:
        form = AddBookForm

    return render(request, 'blog/books/add_book.html', {'form': form})




