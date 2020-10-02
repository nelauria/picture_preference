import requests
from bs4 import BeautifulSoup


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
