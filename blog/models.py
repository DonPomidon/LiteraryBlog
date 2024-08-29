from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique_for_date='publish', unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_added_book')
    publish = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def update_rating(self):
        ratings = UserRating.objects.filter(book=self)
        if ratings.exists():
            self.rating = ratings.aggregate(average_rating=models.Avg('rating'))['average_rating']
        else:
            self.rating = 0.0
        self.save()

    def get_absolute_url(self):
        return reverse('blog:book_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            counter = 1
            while Book.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Review by {self.user.username} - {self.book.title}'

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)


class UserRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'Rating: {self.rating} by {self.user.username} for {self.book.title}'

