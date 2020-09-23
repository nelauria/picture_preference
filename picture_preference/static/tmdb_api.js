function tmdb_search() {
    let apiKey, input, query, main_url, xmlHttp, searchResponse, div, ul, titles = [], images = [];
    apiKey = new XMHttpRequest();
    apiKey.open( "GET", "/")
    input = document.getElementById("userInput").value;
    query = input.replace(" ","%20");
    main_url = "https://api.themoviedb.org/3/search/movie?api_key="+apiKey+"&language=en-US";
    main_url += "&query="+query+"&page=1&include_adult=false";
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", main_url, false);
    xmlHttp.send();
    searchResponse = JSON.parse(xmlHttp.response);
    ul = document.getElementById("film-list");
    films = ul.getElementsByTagName("button");
    images = ul.getElementsByTagName("img");
    for (let i=0; i < 5; i++) {
        var result = searchResponse.results[i]
    	titles.push(result.title.italics()
        	+ " (" + result.release_date.slice(0,4) + ")");
        films[i].innerHTML = titles[i];
        films[i].value = result.title + " (" + result.release_date.slice(0,4) + ")"
        if (searchResponse.results[i].poster_path) {
            images[i].src = "https://image.tmdb.org/t/p/w92/"+searchResponse.results[i].poster_path;
        } else {
            images[i].src = "/static/photo-placeholder-icon-17.jpg"
        }
    }
//    document.getElementById("test").innerHTML = result.title + " (" + result.release_date.slice(0,4) + ")"
    div = document.getElementById("search-results");
    div.style.display = "block";
}
