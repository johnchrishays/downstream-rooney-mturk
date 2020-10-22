# Amazon Mechanical Turk Experiment for "The Effect of the Rooney Rule on Implicit Bias in the Long Term"

To run the web application:

1. Fork or clone this repo.
2. Install the [Django web framework](https://docs.djangoproject.com/en/3.1/) (Make sure you have python 3.7 installed locally.)
3. Install dependencies by running
```
pip install -r requirements.txt
```
in your terminal.
4. Sign up for a [Heroku](https://signup.heroku.com/) account, and follow the instructions [here](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) to install Heroku command line tools and create the application on Heroku. This also creates a Git remote and associates it with your app.
5. Next, set up a database through [Heroku postgres](https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres) 
6. Create an environment variable in your preferred shell called `DATABASE_URL` point to the Heroku postgres database you just created. (If you'd like to run the web application locally only, you can instead [create a postgres database locally](https://www.postgresql.org/docs/13/tutorial-start.html) and point `DATABASE_URL` to your local database.) If you are using bash, you can put the following line at the end of your .bash_profile:
```
export DATABASE_URL="$(heroku config:get DATABASE_URL -a downstreamrooney)"
``` 
7. To make view the application locally, you can run 
```
python manage.py runserver
```
or push the changes to your Heroku app with
```
git push heroku main
```

