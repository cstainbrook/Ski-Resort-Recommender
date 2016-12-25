# Ski-Resort-Recommender

### What's in this Repo
This repo contains the code for a ski resort recommender I made to practice using graphlab and to improve my recommender skills.  The recommender is hosted on [cooperschairlift.com](cooperschairlift.com).

### Replicating the Project

##### Run user_scraper.py
This code scrapes [onthesnow.com](onthesnow.com) for the resort reviews that are used in the recommender.  This code takes awhile to run, as it is scraping all of the reviews on the website.

##### Run recommender.py
This code develops the backend model for the recommender.  It creates two models, a factorization model and a content-based model, which are stored in the models folder.  The factorization model is the model used on the website.

##### Run ski_app.py
This develops the web app, which is hosted on [cooperschairlift.com](cooperschairlift.com).
