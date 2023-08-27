from decouple import config
from datetime import datetime
from pyarr import RadarrAPI
from pyarr.types import JsonObject

class MovieObj:

    def __init__(self, movie_json):
        # General overview
        self.title = f"{movie_json.get('title', None)} ({movie_json.get('year', None)})"
        self.synopsis = movie_json.get('overview', None)
        self.genres = ', '.join(movie_json.get('genres', None))
        self.runtime = f"{movie_json.get('runtime', None)//60}h{movie_json.get('runtime', None)%60}"

        # Status
        self.has_file = movie_json.get('hasFile', None)
        self.status = movie_json.get('status', None)
        self.inCinemas = movie_json.get('inCinemas', None)
        if self.inCinemas:
            date_object = datetime.strptime(self.inCinemas, '%Y-%m-%dT%H:%M:%SZ')
            self.date_released = date_object.strftime('%d/%m/%Y')
        else:
            self.date_released = None

        # Poster
        if "images" in movie_json and movie_json['images']:
            self.poster_image = movie_json['images'][0]['remoteUrl']
        else:
            self.poster_image = ''

        # IDs
        self.trailer_id = movie_json.get('youTubeTrailerId', None)
        # BUG: IMDB ID not working for some reason
        self.imdb_id = movie_json.get('imdbId', None)
        self.tmdb_id = movie_json.get('tmdbId', None)
        self.tmdb_clean_title = movie_json.get('cleanTitle', None)

        # URLs
        self.website_url = movie_json.get('website', None)
        if self.trailer_id:
            self.trailer_url = f"https://youtube.com/watch?v={self.trailer_id}"
        if self.imdb_id:
            self.imdb_url = f"https://imdb.com/title/{self.imdb_id}/"
        if self.tmdb_id and self.tmdb_clean_title:
            self.tmdb_url = f"https://themoviedb.org/movie/{self.tmdb_id}-{self.tmdb_clean_title}/"

class RadarrClient:

    def __init__(self):
        self.ip = str(config('HOST_IP'))
        self.port = str(config('RADARR_PORT'))
        self.url = f"http://{self.ip}:{self.port}/"
        self.api_key = str(config('RADARR_API'))
        self.client = RadarrAPI(
            host_url = self.url,
            api_key = self.api_key
        )
        self.quality_profiles = self.client.get_quality_profile()

    def search_movie(self, search: str):
        self.search_array = self.client.lookup_movie(term = search)
        return self.search_array
    
    def def_array_movies(self, search: str):
        self.movies_list = []
        json_array = self.search_movie(search)
        for array in json_array:
            self.movies_list.append(MovieObj(array))

    def get_free_root_folder(self) -> None:
        self.root_folder_list = self.client.get_root_folder()

    def add_movie(
        self,
        movie
        ) -> JsonObject:
        # import json
        # print(json.dumps(RadarrAPI.get_root_folder, indent=4))
        # print(self.client.get_root_folder())
        self.get_free_root_folder()
        return self.client.add_movie(
            movie = movie,
            quality_profile_id = self.quality_profiles[0].get('id'),
            root_dir = self.root_folder_list[0].get('path')
        )
