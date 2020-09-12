from bs4 import BeautifulSoup
import requests
import re
from movieapp.models import Movie
from movieapp import models
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    url = 'http://www.imdb.com/chart/top'

    response = requests.get(url)

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
                                                    release_year = year,
                                                    imdb_rating=ratings[index],
                                                    movie_crew = crew[index],
                                                    total_votes= votes[index],
                                                    movie_location=place)[0]
            new_movie.save()
            print('%s movie added' % (movie_title,))
        except:
            print('%s movie already exists and has been updated' % (movie_title,))

    self.stdout.write('Movie Added/Updated')
