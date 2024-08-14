from django.urls import path
from .import views


app_name = 'blog'


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/review/', views.book_review, name='book_review'),
    path('about/', views.blog_about, name='blog_about'),
    path('contacts/', views.blog_contacts, name='blog_contacts'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
]
