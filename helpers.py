import base64, re, requests, urllib
from bs4 import BeautifulSoup

def getAccessToken(clientID, clientSecret):

    """
    Get access token for Spotify API

        Parameters:
            clientID (str): unique identifier of app
            clientSecret (str): key used to authorize app
        
        Returns:
            accessToken (str): key used to make requests to Spotify Web API
    """

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

    """
    Convert ASCII string to Base64 string

        Parameters:
            ascii_str (str): string in ASCII format

        Returns:
            base64_str (str): string in Base64 format
    """

    # Convert ASCII string to ASCII bytes
    ascii_bytes = ascii_str.encode('ascii')
    # Convert ASCII bytes to Base64 bytes
    base64_bytes = base64.b64encode(ascii_bytes)
    # Convert Base64 bytes to Base64 string 
    base64_str = base64_bytes.decode('ascii')

    return base64_str

def getPodcastEpisodes(token, podcastID):

    """
    Get all episodes for given podcast
    
        Parameters:
            token (str): key used to make requests to Spotify Web API
            podcastID (str): unique identifier of the show

        Returns:
            episodeList ([str]): list of podcasts episodes
    """

    # Initialze variables 
    episodeList = []
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
        response = requests.get(podcastEndpoint, headers=getHeader).json()["items"]

        # Exit loop once all episodes queried
        if len(response) == 0:
            break

        # Add to list of movie titles
        for episode in response:
            episodeList.append(episode["name"].strip())
        
        # Offset next query 
        offset += len(response)

    return episodeList

def getMovieTitle(episodeTitle):

    """
    Extract movie title from episode title

        Parameters:
            episodeTitle (str): title of podcast episode 

        Returns:
            movieTitle (str): title of movie reviewed in podcast episode
    """

    # Ignore introduction episodes and repeat movies
    ignoreEpisodes = ["Intro: 'The Rewatchables'",
                      "“The Re-Heat” With Bill Simmons and Chris Ryan", 
                      "Welcome to The Rewatchables", 
                      "Miami Vice: Calderone’s Return (Part 1 + 2)",
                      "“The Re-Departed” With Bill Simmons, Chris Ryan, and Sean Fennessey",
                      "The Three-'Heat' With Bill Simmons, Chris Ryan, and Michael Mann",
                      "The New Categories Selection Show",
                      "Creed With Bill Simmons, Wesley Morris, Sean Fennessey, and K. Austin Collins"] # already reviewed
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
    # Missing opening aporstrophe in movie title 
    elif movieTitle[0] != "":
        movieTitle = movieTitle[0]
    # Apostrophe in movie title
    else:
        movieTitle = movieTitle[1] + "\'" + movieTitle[2]

    # Remove unncessary trailing comma if exists
    movieTitle = movieTitle.replace(",", "")

    return movieTitle

def getStreamProviders(movie_title, driver):

    """
    Use Chrome driver to scrape JustWatch website for movie's streaming providers

        Parameters:
            movie_title (str): title of movie to web scrape streaming availability
            driver (Selenium WebDriver): used to write automated web application UI tests against HTTP websites

        Returns:
            streamProviders ([str]): list of streaming providers for the movie
    """

    # Search for movie
    movie_title_parsed = urllib.parse.quote(movie_title)
    url = f"https://www.justwatch.com/us/search?q={movie_title_parsed}"
    driver.get(url)

    # Extract HTML once webpage loads
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        first_result = soup.find("div", {"class":"title-list-row__row title-list-row__row__search"})
        if first_result!= None:
            break
    stream_container = first_result.find("div",{"class":"buybox-row stream inline"})
    if stream_container == None:
        # Not available to stream
        return [""]
    stream_items = stream_container.find("div",{"class": "buybox-row__offers"}).find_all("a", recursive=False)
    if stream_items == []:
        # JustWatch bug - stream container exists, but no elements listed (i.e. The Godfather Part II/III)
        return [""]

    # Create list of streaming providers
    streamProviders = []
    for item in stream_items:
        provider = item.picture.img["alt"]
        streamProviders.append(provider)

    return streamProviders
