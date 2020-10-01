"use strict";

search()

function search(){
    $("input").on("change paste keyup", function () {
        let inputText = $("input").val()
        if(inputText.length >= 2){
            resetSearchResults();
            $.get(
                `http://localhost:5000/api/v1/search?query=${inputText}`,
                function (response) {
                //    build results view here
                    let tableHtml = "<table>"
                    console.log(response);
                    let result;
                    for (result of response){
                        tableHtml += `<td><a href="${result['Resource Url']}"><img src='${result['Image Url']}'></a></br>${result['Artist Name']}</br>${result['Resource Name']}</td>`;
                    }
                    tableHtml += "</table>";
                    // remove loading animation
                    $('.loading-gif').remove()
                    // input results on page
                    $('#main_container').append("<h2>Results</h2>");
                    $('#main_container').append( tableHtml);
                }
            )
        }
    });
}

function resetSearchResults(){
    // remove current results on page if it exists
    $('table').remove();
    $('h2').remove();
    // add loading animation to page
    $('#main_container').append(`<img class= "loading-gif" 
src="static/gifs/Ball-0.5s-200px.gif">`);
}