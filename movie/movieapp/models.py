from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Movie(models.Model):
    movie_name = models.CharField(max_length=300)
    release_year = models.PositiveIntegerField(null=True,blank=True)
    imdb_rating = models.FloatField(null=True,blank=True)
    movie_crew = models.CharField(max_length=500, default='Not Available')
    total_votes= models.PositiveIntegerField(default=0,null=True,blank=True)
    movie_location=models.CharField(max_length=120,default='Not Available')

    def __str__(self):
        return self.movie_name

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wished_movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.wished_movie

class AddingMovies(models.Model):
    url_add=models.URLField()

    def __str__(self):
        return self.url_add
