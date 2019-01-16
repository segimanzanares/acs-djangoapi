# acs-djangoapi
Testing django 2.1 + api rest + oauth2 + postgresql database

## Installation guide

Create virtualenv inside the project root directory, the `-p` argument specifies the path to the python interpreter to be used.
```
$ virtualenv -p /usr/bin/python3.7 ve
```
Activate virtualenv and install dependencies
```
$ source ve/bin/activate
$ pip install -r requirements.txt
```
Edit database settings in `src/main/settings.py`
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

Run migrations
```
$ python src/manage.py migrate
```
Create a superuser
```
$ python src/manage.py createsuperuser
```

Run server
```
$ python src/manage.py runserver
```
Go to http://localhost:8000/admin/oauth2_provider/application/ and create a new application without selecting user, set `client type` to `public`, set `Authorization grant type` to `Resource owner password-based` and enter a name. The `client_id` and `client_secret` data will be used to request tokens with your `username` and `password`.

Request an access token
```
$ curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/oauth/token/
```

Retrieve listing of shows
```
$ curl -H "Authorization: Bearer <your_access_token>" http://localhost:8000/api/v1/shows/
```

Create new show
```
curl -X POST \
  http://localhost:8000/api/v1/shows/ \
  -H 'Content-Type: application/json' \
  -d '{
	"title": "test"
}'
```
