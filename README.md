# The Restreamables
## Video Demo: 
https://youtu.be/K31IDwSUWjw
## Description: 
Determine streaming availability of movies reviewed in "The Rewatchables" podcast.
## Background: 
When I am deciding what movie to watch, I reference movies reviewed in "The Rewatchables" podcast. This process entails searching through the podcast episode list for a movie that interests me and then searching the internet to see what streaming service it is offered on. If it is offered on a service I am subscripted to, then great! If not, then I have to repeat the process. My end goal with this project was to be able to select a streaming service and see what movie's that service offers that have also been reviewed on the podcast. 
## Project Breakdown:
### Spotify API: 
Authenticated application with Spotify and used application ID's to obtain an access token. Once access token is granted, it is used to request data, specifically the title for each episode. The API returns the data in JSON format. 
### Cleaning Data:
The movie title needs to be extracted from the podcast episode titles. This was accomplished using Python's regular expressions module. Corrections had to be made for inconsistent data. For example, some movies are quoted in the podcast episode title with single quotes, and others with double quotes. In addition, some episodes do not even review a movie, such as the "introduction" episodes. Finally, a movie reviewed twice in two separate episodes only needs to be added to the database once. 
### Web Scrape
http://www.justwatch.com/ is webscrapped to obtain the streaming status of each movie. The code executes at the speed the web page is loaded - it will only move on to the next movie once the HTML has loaded. Used Selenium to account for HTML being loaded dynamically with Javascript. Used Beautiful Soup to extract desired HTML. 
### SQL
Stored data in a one-to-many SQL database with two tables. Tables are linked together via a movie id. SQL queries are used to display information on webpage.
### Flask
Locally hosted website. HTML generated using Jinja. 
## References:

- Spotify API
    - https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    - https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-shows-episodes
    - https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/
    - https://www.youtube.com/watch?v=9mKAAWRheTA
    - https://www.youtube.com/watch?v=g6IAGvBZDkE
- Web scraping videos
    - https://www.youtube.com/watch?v=XQgXKtPSzUI
    - https://www.youtube.com/watch?v=gRLHr664tXA
