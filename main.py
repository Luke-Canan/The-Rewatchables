from helpers import getAccessToken, getMovieTitle, getPodcastEpisodes, getStreamProviders
from secrets import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import csv
import sqlite3

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
service = Service(CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(service=service, options=options)

# Collect streaming data for each movie
streaming_data = []
providers_list = []
for movie in movieList:
    providers = getStreamProviders(movie, driver)
    for p in providers:
        if p not in providers_list and p != "":
            providers_list.append(p)
    item = {
        "movie": movie,
        "providers": providers
    }
    streaming_data.append(item)
    print(item)

# End Chrome webdriver
driver.quit()

# Initialize SQL
connection = sqlite3.connect("movie_db")
cursor = connection.cursor()

# Create tables
cursor.execute("CREATE TABLE movies (id INTEGER PRIMARY KEY, movie_title TEXT)")
connection.commit()
cursor.execute("CREATE TABLE streamers (movie_id INTEGER , streamer TEXT, FOREIGN KEY(movie_id) REFERENCES movies(id))")
connection.commit()

# Populate database
for movie in streaming_data:
    cursor.execute("INSERT INTO movies (movie_title) VALUES(?)", (movie["movie"],))
    connection.commit()
    # 
    movie_id = cursor.lastrowid
    for streamer in movie["providers"]:
        cursor.execute("INSERT INTO streamers (movie_id, streamer) VALUES(?, ?)", (movie_id, streamer))
        connection.commit()
        
# End connection
connection.close()
