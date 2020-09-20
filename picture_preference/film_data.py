from picture_preference import web_scrape


def check_popularity(href):
    main = 'https://letterboxd.com'
    url = web_scrape.search_film(query)
    href = url.replace(main, '')
    page = 1
    films = web_scrape.top()
    while href not in films.href.values:
        page += 1
        films = web_scrape.top(page=page).set_index(films.index+72)
    film_info = films.loc[films.href == href]
    rank = film_info.index[0]+1
    # print(f'{film_info.Title.iloc[0]} is ranked #{rank} in popularity.')
    total_films = 542018
    obscurity = (film_info.index[0]/total_films)*100
    # print(f'{film_info.Title.iloc[0]} is more obscure than {obscurity:.5f}% of films on Letterboxd.')
    return [film_info.Title.iloc[0], rank, obscurity]

