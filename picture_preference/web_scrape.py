from bs4 import BeautifulSoup
from flask import current_app
import requests


def tmdb_id(title_year):
    api_key = current_app.config["TMDB_KEY"]
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US"
    # print(title_year)
    title = title_year[:-7]
    title = title.replace(" ", "%20").replace("#", "%23")
    try:
        year = int(title_year[-5:-1])
    except ValueError:
        year = None
    if year:
        search_url = search_url + f"&query={title}&page=1&include_adult=false&year={year}"
    else:
        title = title_year
        title = title.replace(" ", "%20").replace("#", "%23")
        search_url = search_url+f"&query={title}&page=1&include_adult=false"
    response = requests.get(search_url)
    results = response.json()["results"]
    if not results:
        print(f"Year mismatch for {title_year}, searching in {year+1}...")
        search_url = search_url + f"&query={title}&page=1&include_adult=false&year={year+1}"
        response = requests.get(search_url)
        results = response.json()["results"]
        if not results:
            print(f"Another year mismatch, searching in {year-1}...")
            search_url = search_url + f"&query={title}&page=1&include_adult=false&year={year-1}"
            response = requests.get(search_url)
            results = response.json()["results"]
            if not results:
                print(f"Another year mismatch, searching in TV...")
                search_url = search_url.replace("/movie?", "/tv?")
                response = requests.get(search_url)
                results = response.json()["results"]
                if not results:
                    print(f"No results for {title_year}, film_id = 0.")
                    film_id = 0
                    return film_id
    film_id = results[0]["id"]
    return film_id


def meta_soup(film_id):
    api_key = current_app.config["TMDB_KEY"]
    details_url = f"https://api.themoviedb.org/3/movie/{film_id}?api_key={api_key}&language=en-US&append_to_response=keywords,credits"
    response = requests.get(details_url)
    details = response.json()
    genres = [i["name"].replace(" ", "").lower() for i in details["genres"]]
    keywords = [i["name"].replace(" ", "").lower() for i in details["keywords"]["keywords"]]
    cast = [details["credits"]["cast"][i]["name"].replace(" ", "").lower() for i in range(0, 3)]
    directors = [i["name"].replace(" ", "").lower() for i in details["credits"]["crew"] if i["job"] == "Director"]
    metadata = genres + keywords + cast + directors
    soup = " ".join(metadata)
    return soup


def top_pages(time_period='', start_page=1, end_page=10):
    titles = []
    ranks = []
    hrefs = []
    tmdb_ids = []
    film_meta = []
    for page_num in range(start_page, end_page+1):
        url = 'https://letterboxd.com/films/ajax/popular/'+time_period+'/size/small/'
        if page_num != 1:
            url = url+f'page/{page_num}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        films_divs = soup.find_all(title=True)
        iter_range = range(len(films_divs))
        for i in iter_range:
            film_div = films_divs[i]
            title = film_div['title']
            titles.append(title)
            hrefs.append(film_div['href'])
            tmdb_id_i = tmdb_id(title)
            tmdb_ids.append(tmdb_id_i)
            film_meta.append(meta_soup(tmdb_id_i))
            ranks.append(i+1+(page_num-1)*72)
    return titles, ranks, hrefs, tmdb_ids, film_meta
