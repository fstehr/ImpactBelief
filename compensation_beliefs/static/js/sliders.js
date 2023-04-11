// get js vars from python
let first_round_part3 = js_vars.first_round_part3;
let round_number = js_vars.round_number;
let role = js_vars.role;
let max_compensation = js_vars.max_compensation;




// display current value next to slider
$(function()
{
$('.slider').on('input change', function(){
    $(this).next($('.slider_label')).html(this.value);
     });
    $('.slider_label').each(function(){
          var value = $(this).prev().attr('value');
        $(this).html(value);
     });
})




// on form submission, check that all elements have been moved
function checkTouched() {
    var sliders = document.getElementsByClassName("slider2");
    // console.log("length of sliders list in class slider 2", sliders.length)
    // in part 2 check only slider length
    if (sliders.length !== 0) {
        prevent_submission();
    } else if (round_number >= first_round_part3) { // check also compensation belief but only in part 3
        if (role === "Person A" && (document.getElementById("compensation_belief").value === "" ||
            document.getElementById("compensation_belief").value <0 ||
                document.getElementById("compensation_belief").value > max_compensation)) {
            prevent_submission();
        } else if (role === "Person A2" && (document.getElementById("compensation_belief_buyer2").value === "" ||
            document.getElementById("compensation_belief_buyer2").value <0 ||
                document.getElementById("compensation_belief_buyer2").value > max_compensation)) {
            prevent_submission();
        }
        else {
            form.submit();
        }
    }
}

function prevent_submission() {
    event.preventDefault();
    window.scrollTo(0, 0);
    document.getElementById('alert').style.display = "block";
}

// define touched as counter with eventlistener on change
touched = 0

function set_touched(event) {
    touched += 1;
    console.log("touched counter is", touched);
    this.className = "slider";
    this.removeEventListener('mouseup', set_touched);
    document.getElementById('belief').style.visibility = "visible";
    }

var sliders = document.getElementsByClassName("slider2");
    for (i = 0; i < sliders.length; i++) {
        sliders[i].addEventListener('mouseup', set_touched);
    }

/* get current values from slider to display underneath slider input */
function displaycurrent() {
    belief1 = Number(document.getElementById("buy_belief").value);
    /* parse to html */
    document.getElementById("current_belief").innerHTML = belief1;
}
function displaycurrent2() {
    belief2 = Number(document.getElementById("buy_belief_buyer2").value);
    /* parse to html */
    document.getElementById("current_belief").innerHTML = belief2;
}





