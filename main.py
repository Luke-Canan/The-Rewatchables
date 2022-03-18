from helpers import getAccessToken, getPodcastEpisodes, getStreamProviders, getMovieTitle
from secrets import *
from selenium import webdriver

# Get Spotify API access token
token = getAccessToken(clientID, clientSecret)

# Get list of "The Rewatchables" podcast episodes
podcastID = "1lUPomulZRPquVAOOd56EW"
episodeList = getPodcastEpisodes(token, podcastID)

# Create list of movie titles
movieList = []
for episodeTitle in episodeList:
    movie = getMovieTitle(episodeTitle)
    if movie != None:
        movieList.append(movie)

# Initialize Chrome webdriver
PATH = "/Applications/chromedriver"
driver = webdriver.Chrome(PATH)

# Populate database with movie title and streaming providers
movie_db = []
for movie in movieList:
    item = {
        "movie": movie,
        "providers": getStreamProviders(movie, driver)
    }
    movie_db.append(item)
    print(item)