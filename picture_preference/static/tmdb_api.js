$(document).on('input touchend', '#userInput', function(){
//    var input = $(this).val();
//    let div, ul, titles = [], images = [];
//    $.ajax({
//        url: $SCRIPT_ROOT + "_search",
//        type: "get",
//        data: {searchQuery: input},
//        dataType: "text",
//        success: function(data) {
//            dataJSON = JSON.parse(data)
//            $.each(dataJSON, function(index, item) {
//                title = item.title
//                buttonText = title.italics() + " (" + item.release_date.slice(0,4) + ")";
//                if (item.poster_path) {
//                    posterLink = "https://image.tmdb.org/t/p/w92/" + item.poster_path;
//                } else {
//                    posterLink = "/static/photo-placeholder-icon-17.jpg"
//                }
//                $(".film-button").eq(index).html(buttonText)
//                $(".film-button").eq(index).attr("value", title + " (" + item.release_date.slice(0,4) + ")")
//                $(".poster").eq(index).attr("src", posterLink)
//            })
//            if (data !== '[]') {
//                $(".search-results").css("display", "block")
//            }
////            $("#test").html("changed")
//        }
//    })
    $("#test").html("changed")
});

