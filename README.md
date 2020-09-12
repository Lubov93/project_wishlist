

User can create accounts and login 
Home page: localhost
movie list: localhost/movie/list 
wish list: localhost/movie/wishlist (login required)
Signup: localhost/accounts/signup -> 



Firstly Create the Virtual enviornment

1.virtualenv -p python3 env
2.source env/bin/activate
3.cd movie
4.pip install -r requirement.txt
5.python manage.py runserver
Then makemigrations are required:

--> $ python manage.py makemigrations --> $ python manage.py migrate

Now run server by

--> $ python manage.py runserver

if the local IP address shows refused to connect --> $ python manage.py runserver 127.0.0.1:8000

If you start this project localy:
!!Change in settings :
1)drop this from settings:
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
If you have another one logs.Just change settings like in documentation.
