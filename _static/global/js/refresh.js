//https://www.aspdotnet-suresh.com/2015/10/jquery-set-open-particular-bootstrap-tab-on-page-load-button-link-click-example.html

// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    classCheck = $('div').hasClass("otree-form-errors alert alert-danger");
    console.log("classCeck", classCheck);

    if ($('div').hasClass("otree-form-errors alert alert-danger")) {
        $('.nav-tabs a:last').tab('show');   // yields Uncaught TypeError: $(...).tab is not a function
    }
});






