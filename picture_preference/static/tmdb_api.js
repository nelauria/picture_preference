function tmdb_search(apiKey) {
    let input, query, main_url, xmlHttp, searchResponse, div, ul, titles = [], images = [];
    input = document.getElementById("userInput").value;
    query = input.replace(" ","%20");
    main_url = "https://api.themoviedb.org/3/search/movie?api_key="+apiKey+"&language=en-US";
    main_url += "&query="+query+"&page=1&include_adult=false";
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", main_url, false);
    xmlHttp.send( null );
    searchResponse = JSON.parse(xmlHttp.response);
    ul = document.getElementById("film-list");
    films = ul.getElementsByTagName("button");
    images = ul.getElementsByTagName("img");
    for (let i=0; i < 5; i++) {
        let result = searchResponse.results[i]
    	titles.push(result.title.italics()
        	+ " (" + result.release_date.slice(0,4) + ")");
        films[i].innerHTML = titles[i];
        films[i].value = result.title[i].replace(" ","-").toLowerCase() + "-" + result.release_date.slice(0,4)
        images[i].src = "https://image.tmdb.org/t/p/w92/"+searchResponse.results[i].poster_path;
    }
    div = document.getElementById("search-results");
    div.style.display = "block";
}
