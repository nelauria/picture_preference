require('dotenv').config();
function tmdb_search() {
    var query, main_url, xmlHttp, searchResponse, titles = [];
    const api_key = process.env.TMDB_API_KEY;
    query = document.getElementById("film").replace(" ","%20");
    main_url = "https://api.themoviedb.org/3/search/movie?api_key="+api_key+"&language=en-US";
    main_url += "&query="+query+"&page=1&include_adult=false";
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", main_url, false);
    xmlHttp.send( null );
    searchResponse = JSON.parse(xmlHttp.response);
    for (let i=0; i < 5; i++) {
    	titles.push(searchResponse.results[i].title
        	+ " (" + searchResponse.results[i].release_date.slice(0,4) + ")");
        var list = document.getElementsByTagName("ul")[0];
        list.getElementsByTagName["li"][i].innerHTML = titles[i];
        var div = document.getElementById("film-list");
        div.style.display = "block";
    }
}
