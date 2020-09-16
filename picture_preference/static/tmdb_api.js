require('dotenv').config();
const api_key = process.env.TMDB_API_KEY
function tmdb_search() {
    var input = document.getElementById("testInput");
    var query = input.replace(" ","%20");
    var main_url = "https://api.themoviedb.org/3/search/movie?api_key="+api_key+"&language=en-US";
    main_url += "&query="+query+"&page=1&include_adult=false";
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", main_url, false);
    xmlHttp.send( null );
    var searchResponse = JSON.parse(xmlHttp.response);
    var firstFive = searchResponse.results.slice(0,5);
    var i;
    var titles = [];
    var div = document.getElementById("searchBar")
    var a = div.getElementsByTagName("a")
    for (i=0; i < firstFive.length; i++) {
    		titles.push(firstFive[i].title
        	+ " (" + firstFive[i].release_date.slice(0,4) + ")");
        a[i].innerHTML = titles[i]
    }
    document.getElementById("test").innerHTML = titles;
}