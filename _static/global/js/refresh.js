//https://www.aspdotnet-suresh.com/2015/10/jquery-set-open-particular-bootstrap-tab-on-page-load-button-link-click-example.html

// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );

    classCheck = $('div').hasClass("otree-form-errors alert alert-danger");
    console.log("classCeck", classCheck);

    if ($('div').hasClass("otree-form-errors alert alert-danger")) {
        $('.nav-tabs a:last').tab('show');   // show last tab
    }
});

var startTime = new Date().getTime();
console.log("Time printed is", startTime)

function resetTabs(){
    time_clicked = new Date().getTime();
    time_spent_in_sec = (time_clicked - startTime)/1000
    console.log("time spent in secs is", time_spent_in_sec)

    if ((time_spent_in_sec < 60) && !($('div').hasClass("otree-form-errors alert alert-danger"))){
        event.preventDefault();
        alert("Please take your time to read the instructions before answering the comprehension questions.");
        console.log("btn clicked too early")
        let early_click = document.getElementById("clicked_early");
        early_click.value = "True";
    }

}







