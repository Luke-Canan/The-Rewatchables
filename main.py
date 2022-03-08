from helpers import getAccessToken, getPodcastEpisodes, movieTitle
from secrets import *

# Get Spotify API access token
token = getAccessToken(clientID, clientSecret)

# Get list of "The Rewatchables" podcast episodes
podcastID = "1lUPomulZRPquVAOOd56EW"
episodeList = getPodcastEpisodes(token, podcastID)

# Create list of movie titles
movieList = []
for episodeTitle in episodeList:
    movie = movieTitle(episodeTitle)
    if movie != None:
        movieList.append(movie)

# Print each movie to terminal
for movie in movieList:
    print(movie)