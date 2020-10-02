$(document).on('input touchend', '#userInput', function(){
    var input = $(this).val();
    let div, ul, titles = [], images = [];
    $.ajax({
        url: $SCRIPT_ROOT + "_search",
        type: "get",
        data: {searchQuery: input},
        dataType: "text",
        success: function(data) {
            let dataJSON = JSON.parse(data)
            $.each(dataJSON, function(index, item) {
                title = item.title
                buttonValue = title + " (" + item.release_date.slice(0,4) + ")";
                buttonText = title.italics() + " (" + item.release_date.slice(0,4) + ")";
                if (item.poster_path) {
                    posterLink = "https://image.tmdb.org/t/p/w92/" + item.poster_path;
                } else {
                    posterLink = "/static/photo-placeholder-icon-17.jpg";
                }
                $(".film-button").eq(index).html(buttonText);
                $(".film-button").eq(index).attr("value", buttonValue);
                $(".poster-button").eq(index).css("background-image", "url(" + posterLink + ")");
                $(".poster-button").eq(index).attr("value", buttonValue);
            })
            if (data !== '[]') {
                $(".search-results").css("display", "block");
            }
        }
    })
//    $("#test").html("changed")
});

$(document).on("focus", "#userInput", function(){
//    $("#test").html("changed")
    if ($(window).width() <= 650) {
        $(".explain").css("height", 0);
    }
});
