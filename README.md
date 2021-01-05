# Url Shortener

Using Flask framework, I create a local host web service that will take in any urls and store them in sqlite database using Flask-Sqlalchemy with their short url. The short url also can be used to retrieve the original one. The app also requires authentication using Oauth 2.0 google authentication (Auth_lib).

# Install requirement
Execute the command below to install requirement packages:

```pip3 install -r requirements.txt```

# Configuration
I use dotenv to manipulate environment variable, a .env file must be created in order to run the app.

.env file should look like:

```
FLASK_APP=app
FLASK_SECRET_KEY=<secretkey>
FLASK_ENV=development
OAUTHLIB_INSECURE_TRANSPORT=true
OAUTHLIB_RELAX_TOKEN_SCOPE=true
GOOGLE_CLIENT_ID=<client id generated by google cloud oauth 2.0 service>
GOOGLE_CLIENT_SECRET=<secret generated by google cloud oauth 2.0 service>
DATABASE_URL=sqlite:///googleauth.sqlite3
CONF_URL=https://accounts.google.com/.well-known/openid-configuration
```


# Run the app

Create database table for ORM:

``` flask create_db ```

Run the app:

```flask run```
