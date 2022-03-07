from helpers import getAccessToken, getPodcastEpisodes
from secrets import *

# Get Spotify API access token
token = getAccessToken(clientID, clientSecret)

# Get list of "The Rewatchables" podcast episodes
podcastID = "1lUPomulZRPquVAOOd56EW"
movieList = getPodcastEpisodes(token, podcastID)

# Print each movie to terminal
for movie in movieList:
    print(movie)
