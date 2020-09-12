from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
                        LoginRequiredMixin,
                        PermissionRequiredMixin
                        )
from django.views import generic
from . import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect,render
from django.http import HttpResponse, JsonResponse
#for function based view
from rest_framework.parsers import JSONParser
from .serializers import MovieSerializer, WishlistSerializer, URLSerializer
from django.views.decorators.csrf import csrf_exempt
#generic view
from rest_framework import generics, mixins
#for Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from bs4 import BeautifulSoup
import requests
import re
from movieapp.models import Movie
from movieapp import models
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from django.contrib.auth import get_user_model
User = get_user_model()

#for Manually Movie Adding API

class MovieListView(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin

                    ):
    serializer_class = MovieSerializer
    queryset = models.Movie.objects.all()

    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# For Editing a Movie API

class MovieDetailView(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin

                    ):
    serializer_class = MovieSerializer
    queryset = models.Movie.objects.all()

    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


#User Wishlist Checking API

class WishlistListView(generics.GenericAPIView,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin

                    ):

    serializer_class = WishlistSerializer
    queryset = models.Wishlist.objects.all()

    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# User Wishlist Editing API

class WishlistDetailView(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin

                    ):
    serializer_class = WishlistSerializer
    queryset = models.Wishlist.objects.all()

    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

#Scrapping URL
class URLView(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin

                    ):
    serializer_class = URLSerializer
    queryset = models.AddingMovies.objects.all()



    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        new_url=request.POST['url_add']

        final=str(new_url)


        response = requests.get(final)

        soup = BeautifulSoup(response.text, 'lxml')

        movies = soup.select('td.titleColumn')
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

        for index in range(0, len(movies)):
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index))+1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index))-(len(movie))]


            try:
                new_movie = Movie.objects.get_or_create(movie_name=movie_title,
                                                        )[0]
                new_movie.save()
                new_movie.release_year = year
                new_movie.imdb_rating=ratings[index]
                new_movie.movie_crew = crew[index]
                new_movie.total_votes= votes[index]
                new_movie.movie_location=place
                new_movie.save()
                print('%s movie added' % (movie_title,))
            except IntegrityError():
                new_movie = Movie.objects.get(movie_name=movie_title,
                                                        )[0]
                new_movie.save()
                new_movie.release_year = year
                new_movie.imdb_rating=ratings[index]
                new_movie.movie_crew = crew[index]
                new_movie.total_votes= votes[index]
                new_movie.movie_location=place
                new_movie.save()
                print('%s movie already exists and has been updated' % (movie_title     ,))

        return self.create(request)


#Views For User Interface
class ListMovie(generic.ListView):
    model = models.Movie

class SingleMovie(generic.DetailView):
    model = models.Movie

class WishList(generic.ListView):
    model = models.Wishlist


class WishlistView(LoginRequiredMixin,generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'movieapp/wishlist_list.html'
    model = models.Wishlist
    fields = '__all__'

    def get_queryset(self):
        return models.Wishlist.objects.filter().order_by('create_date')

@login_required
def add_to_wishlist(request,pk):

   item = get_object_or_404(models.Movie,pk=pk)

   wished_movie,create = models.Wishlist.objects.get_or_create(wished_movie=item,
   pk = item.pk,
   user = request.user,
   )

   messages.info(request,'Movie added to your wishlist')
   return redirect('wish_list')
