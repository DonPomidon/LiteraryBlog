from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    slug = models.SlugField(max_length=250)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_added_book')
    publish = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = reviews.aggregate(average_rating=models.Avg('rating'))['average_rating']
        else:
            self.rating = 0.0
        self.save()


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()


