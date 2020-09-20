import requests
from bs4 import BeautifulSoup
import pandas as pd


def top(time_period='',page=1):
    url = 'https://letterboxd.com/films/ajax/popular/'+time_period+'/size/small/'
    if page != 1:
        url = url+f'page/{page}/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    films_divs = soup.find_all(title=True)
    films = pd.DataFrame()
    films['Title'] = [films_divs[i]['title'][:-7] for i in range(len(films_divs))]
    films['Year'] = [films_divs[i]['title'][-5:-1] for i in range(len(films_divs))]
    films['href'] = [films_divs[i]['href'] for i in range(len(films_divs))]
    return films


def search_film(query):
    query = str(query).replace(' ','+')
    main = 'https://letterboxd.com'
    search_url = main+f'/search/films/{query}/'
    search_page = requests.get(search_url)
    search_soup = BeautifulSoup(search_page.content,'html.parser')
    try:
        first_result_url = main+search_soup.find(class_='film-detail-content').h2.a['href']
    except:
        raise Exception('The film you searched for was not found. Try searching for a different title.')
    return first_result_url


def get_genres(film_url):
    film_page = requests.get(film_url)
    if not page.status_code:
        raise Exception('The url does not lead to a valid Letterboxd page. '
                        'Make sure you entered the correct url for the film.')
    film_soup = BeautifulSoup(film_page.content,'html.parser')
    genre_links = film_soup.find(id='tab-genres').find_all('a')
    genres = [genre_links[i].string for i in range(len(genre_links))]
    return genres


def top_pages(time_period='', start_page=1, end_page=10):
    titles = []
    ranks = []
    hrefs = []
    for page_num in range(start_page, end_page+1):
        url = 'https://letterboxd.com/films/ajax/popular/'+time_period+'/size/small/'
        if page_num != 1:
            url = url+f'page/{page_num}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content,'html.parser')
        films_divs = soup.find_all(title=True)
        for i in range(len(films_divs)):
            titles.append(films_divs[i]['title'])
            ranks.append(i+1+(page_num-1)*72)
            hrefs.append(films_divs[i]['href'])
    return titles, ranks, hrefs
