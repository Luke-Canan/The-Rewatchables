from helpers import getAccessToken, getMovieTitle, getPodcastEpisodes, getStreamProviders
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
    if movie != None and movie not in movieList:
        movieList.append(movie)

# Initialize Chrome webdriver
CHROMEDRIVER_PATH = "/Applications/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)

# Populate database with movie title and streaming providers
movie_db = []
for movie in movieList:
    item = {
        "movie": movie,
        "providers": getStreamProviders(movie, driver)
    }
    movie_db.append(item)
    print(item)

# End Chrome webdriver
driver.quit()