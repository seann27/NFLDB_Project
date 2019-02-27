$(document).ready( function() {

    $("#trigger").click( function(event) {
        alert("You clicked the first trigger button using JQuery!");
        $.ajax({
            url: "/js_event/1/"
        });
    });

    $("#trigger2").click( function(event) {
        alert("You clicked the second trigger button using JQuery!");
        $.ajax({
            url: "/js_event/2/"
        });
    });

    $("#team_button").click( function(event) {
        $.ajax({
            url: "/js_event/4/"
        });
    });

    $("#roster").click( function(event) {
        var team = document.getElementById("roster").value;
        alert("you selected "+team);
        $.ajax({
            url: ("/js_event/5/"+team+"/"),
        });
    });
});