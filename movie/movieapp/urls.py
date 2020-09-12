from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.ListMovie.as_view(),name='movie_list'),
    path('list/<pk>',views.SingleMovie.as_view(),name='single'),
    path('list/<pk>/add2wishlist',views.add_to_wishlist,name='wishlist'),
    path('wishlist/',views.WishlistView.as_view(),name='wish_list'),
    path('api/', views.MovieListView.as_view(),name='movie_list_api'),
    path('api/detail/<id>', views.MovieDetailView.as_view(),name='movie_detail_api'),
    path('wishlist/api/', views.WishlistListView.as_view(),name='wishlist_api'),
    path('wishlist/api/detail/<id>', views.WishlistDetailView.as_view(),name='wishlist_detail_api'),
    path('addmovies/', views.URLView.as_view(),name='adding_movies'),
]
