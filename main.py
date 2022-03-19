from helpers import getAccessToken, getMovieTitle, getPodcastEpisodes, getStreamProviders
from secrets import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import csv

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

# Output data to csv
keys = streaming_data[0].keys()
with open("data.csv", "w") as output_file:
    writer = csv.DictWriter(output_file, keys)
    writer.writeheader()
    writer.writerows(streaming_data)

for provider in sorted(providers_list, key=str.casefold):
    print(provider)
print(len(providers_list))