from helpers import getAccessToken, getMovieTitle, getPodcastEpisodes, getStreamProviders
from spotifyCodes import clientID, clientSecret
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    connection = sqlite3.connect("movie_db")
    cursor = connection.cursor()
    
    try:
        headers = cursor.execute("SELECT DISTINCT streamer FROM streamers ORDER BY UPPER(streamer)").fetchall()
        return render_template("index.html", headers=headers)
    except:
        return redirect("/update")

@app.route("/movies", methods=["GET"])
def movies():

    provider = request.values.get("providers")

    connection = sqlite3.connect("movie_db")
    cursor = connection.cursor()

    movies = cursor.execute("SELECT movie_title FROM movies WHERE id IN (SELECT movie_id FROM streamers WHERE streamer = ?)", (provider,)).fetchall()

    # movies = cursor.execute("SELECT movie_title FROM movies")

    return render_template("movies.html", movies=movies)

@app.route("/update", methods=["GET"])
def update():

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

    # Delete tables
    cursor.execute("DROP TABLE movies")
    connection.commit()
    cursor.execute("DROP TABLE streamers")
    connection.commit()

    # Create tables
    cursor.execute("CREATE TABLE movies (id INTEGER PRIMARY KEY, movie_title TEXT)")
    connection.commit()
    cursor.execute("CREATE TABLE streamers (movie_id INTEGER , streamer TEXT, FOREIGN KEY(movie_id) REFERENCES movies(id))")
    connection.commit()

    # Populate database
    for movie in streaming_data:
        cursor.execute("INSERT INTO movies (movie_title) VALUES(?)", (movie["movie"],))
        connection.commit()
        movie_id = cursor.lastrowid
        for streamer in movie["providers"]:
            cursor.execute("INSERT INTO streamers (movie_id, streamer) VALUES(?, ?)", (movie_id, streamer))
            connection.commit()

    # End connection
    connection.close()

    return redirect("/")
