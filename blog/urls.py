from django.urls import path
from .import views


app_name = 'blog'


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/review/', views.book_review, name='book_review'),
    path('about/', views.blog_about, name='blog_about'),
    path('contacts/', views.blog_contacts, name='blog_contacts'),
    path('add_book/', views.book_add, name='book_add'),
    path('edit_review/<int:review_id>', views.edit_review, name='edit_review'),
]
