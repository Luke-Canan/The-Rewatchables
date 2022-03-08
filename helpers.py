import requests
import base64, json, re

def getAccessToken(clientID, clientSecret):

    """Get access token for API"""

    # https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/


    # POST request
    authEndpoint = "https://accounts.spotify.com/api/token"
    authHeader = {
        "Authorization": "Basic " + asciiToBase64str(f"{clientID}:{clientSecret}")
    }
    authData = {
        "grant_type": "client_credentials"
    }
    response = requests.post(authEndpoint, headers=authHeader, data=authData)

    # Extract access token from response
    accessToken = response.json()["access_token"]

    return accessToken

def asciiToBase64str(ascii_str):

    """Convert ASCII string to Base64 string"""

    # https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/


    # Convert ASCII string to ASCII bytes
    ascii_bytes = ascii_str.encode('ascii')
    # Convert ASCII bytes to Base64 bytes
    base64_bytes = base64.b64encode(ascii_bytes)
    # Convert Base64 bytes to Base64 string 
    base64_str = base64_bytes.decode('ascii')

    return base64_str

def getPodcastEpisodes(token, podcastID):

    # https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-shows-episodes


    # Initialze variables 
    movieList = []
    getHeader = {
        "Authorization": "Bearer " + token,
    }
    limit = 50
    offset = 0

    # Multiple requests required due to query limit
    while True:

        # GET request
        # Include market in endpoint or else ID will be invalid (Spotify API bug)
        podcastEndpoint = f"https://api.spotify.com/v1/shows/{podcastID}/episodes?market=US&limit={limit}&offset={offset}"
        episodes = requests.get(podcastEndpoint, headers=getHeader).json()["items"]

        # Exit loop once all episodes queried
        if len(episodes) == 0:
            break

        # Add to list of movie titles
        for e in episodes:
            movie = movieTitle(e["name"].strip())
            if movie != None:
                movieList.append(movie)
        
        # Offset next query 
        offset += len(episodes)

    return movieList

def movieTitle(episodeTitle):

    """Extract movie title from episode title"""

    # Ignore introduction episodes and repeat movies
    ignoreEpisodes = ["Intro: 'The Rewatchables'",
                      "“The Re-Heat” With Bill Simmons and Chris Ryan", 
                      "Welcome to The Rewatchables", 
                      "Miami Vice: Calderone’s Return (Part 1 + 2)",
                      "“The Re-Departed” With Bill Simmons, Chris Ryan, and Sean Fennessey",
                      "The Three-'Heat' With Bill Simmons, Chris Ryan, and Michael Mann"]
    if episodeTitle in ignoreEpisodes:
        return None

    # Split episode title by characters that designate the start and end of movie title
    demarcators = "[\u2018|\u2019|\"|\'|\u201C|\u201D]"
    movieTitle = re.split(f"{demarcators}", episodeTitle)

    # No apostrophe in movie title or guest list
    if len(movieTitle) == 3:
        movieTitle = movieTitle[1]
    # Apostrophe in guest list
    elif movieTitle[1].find("The Shawshank Redemption") >= 0 or movieTitle[1].find("Fatal Attraction") >= 0:
        movieTitle = movieTitle[1]
    # Apostrophe in movie title
    else:
        movieTitle = movieTitle[1] + "\'" + movieTitle[2]

    # Remove unncessary trailing comma if exists
    print(movieTitle.replace(",", ""))

    return movieTitle
