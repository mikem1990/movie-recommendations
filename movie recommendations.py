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