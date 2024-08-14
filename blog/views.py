from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm, CreateCustomUser, LoginCustomUser
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def login_user(request):
    if request.method == 'POST':
        form = LoginCustomUser(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('blog:book_list')
            else:
                form.add_error(None, 'Username or password is invalid, try again!')
    else:
        form = LoginCustomUser()

        return render(request, 'blog/books/login.html',
                                    {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = CreateCustomUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:book_list')
        else:
            form.add_error(None, 'Wrong data, try again!')
    else:
        form = CreateCustomUser

    return render(request, 'blog/books/register.html',
                                {'form': form})


def logout_user(request):
    auth_logout(request)
    return redirect('blog:book_list')


def blog_about(request):
    return render(request, 'blog/books/about.html')


def blog_contacts(request):
    return render(request, 'blog/books/contacts.html')


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


