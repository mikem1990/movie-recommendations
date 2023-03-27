import json
import requests_with_caching

# given a movie, get 5 related movies with tastedive (no api key) using provided cache requests
def get_movies_from_tastedive(movie):
    parameters = {"q" : movie, "type" : "movies", "limit" : 5}
    tastedive_response = requests_with_caching.get("https://tastedive.com/api/similar", params = parameters)
    similar_movies_dict = json.loads(tastedive_response.text)
    return similar_movies_dict

# extract movie titles from results in a list
def extract_movie_titles(similar_movies_dict):
    return [i["Name"] for i in similar_movies_dict["Similar"]["Results"]]

# get related movies for list of movies, results combined in a list
def get_related_titles(movies_list):
    recommended_list = []
    for i in movies_list:
        recommended_list.extend(extract_movie_titles(get_movies_from_tastedive(i)))
    return list(set(recommended_list))

# given movie, get movie data from omdb (year released, rating, runtime etc)
def get_movie_data(movie):
    parameters = {"t" : movie, "r" : "json"}
    omdb_response = requests_with_caching.get("http://www.omdbapi.com/", params = parameters)
    movie_data_dict = json.loads(omdb_response.text)
    return movie_data_dict

# get rotten tomatoes rating from movie data or 0 if no rating
def get_movie_rating(movie_data_dict):
    for i in movie_data_dict["Ratings"]:
        if i["Source"] == "Rotten Tomatoes":
            return int(i["Value"][:-1])         # i[Value] is str 'n%', [-1] to remove % sign and convert to int
    return 0

# given a list of movies, get recommended movies and their rotten tomato ratings, sorted non-ascending
def get_sorted_recommendations(movies_list):
    final_recommendations = []
    for i in get_related_titles(movies_list):
        rating_movie = (get_movie_rating(get_movie_data(i)), i)         # save rating and movie as tuple (rating, movie) for easy sorting                 
        final_recommendations.append(rating_movie)
    return [i[1] for i in sorted(final_recommendations, reverse = True)]            # return i[1] for movie title only