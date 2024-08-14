from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    username = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICES,
                              default='MALE')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='Groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


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
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
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
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = reviews.aggregate(average_rating=models.Avg('rating'))['average_rating']
        else:
            self.rating = 0.0
        self.save()

    def get_absolute_url(self):
        return reverse('blog:book_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Review by {self.user.username} - {self.book.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.book.update_rating()



