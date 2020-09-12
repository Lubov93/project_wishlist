from rest_framework import serializers
from .models import Movie, Wishlist, AddingMovies



class MovieSerializer(serializers.ModelSerializer):
    class Meta():
        model = Movie
        fields='__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta():
        model = Wishlist
        fields = '__all__'

class URLSerializer(serializers.ModelSerializer):
    class Meta():
        model = AddingMovies
        fields='__all__'
