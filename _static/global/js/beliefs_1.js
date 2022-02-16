let form = document.getElementById("form");

/* call time variables from python */
let Intro = js_vars.sec_intro * 1000;
let Delay = js_vars.sec_per_matrix * 1000;
let AnswerTime = js_vars.sec_to_answer * 1000;

/* call all elements */
let alert = document.getElementById('alert');
let countdown = document.getElementById("countdown");

let cardA = document.getElementById("cardA");
let matrix1_white = document.getElementById('matrix1_white');
let matrix1 = document.getElementById('matrix1');
let beliefA = document.getElementById("beliefA");
let num_x_belief_A = document.getElementById("num_x_belief_A");
let slider_A = document.getElementById("certainty_A");
let CIA = document.getElementById("CIA");
let count = document.getElementById("count");

let cardC = document.getElementById("cardC");
let donations = document.querySelectorAll("input[type=radio]");

let NextButton1 = document.getElementById("NextButton1");
let SubmitButton = document.getElementById("SubmitButton");

let page_loaded = document.getElementById("page_loaded");


// Function that starts timing on page load (for Panel A)
function HideImageLoadForm() {
    console.log("page was loaded", localStorage.getItem('counter'), "times")
    alert.style.display = "block";
    /* on load disable donation fields */
    var i;
    for (i = 0; i < donations.length; i++) {
        donations[i].disabled = true;
    }

    /* define protocol in seconds */
    // Intro time delay to display matrix A
    setTimeout(function () {
        alert.style.display = "none";
        matrix1_white.style.display = "none";
        matrix1.style.display = "block";

        // after intro show hide matrix after 'Delay' seconds
        setTimeout(function () {
            matrix1.style.display = "none";
            beliefA.style.display = "block";
            cardA.style.color = "black";
            num_x_belief_A.disabled = false;
            slider_A.disabled = false;
            NextButton1.style.display = "block";

            // display count down
            countdown.style.visibility = "visible";
            // set counter for count down equal to answer time secs
            var counter = AnswerTime / 1000;
            setTimeout(function run() {
                counter--;
                // console.log("countdown 1:", counter)
                if (counter >= 0) {
                    count.innerHTML = counter;
                    countdown1 = setTimeout(run, 1000);
                }
                if (counter === 0) {
                    // when countdown is run out disable fields
                    num_x_belief_A.disabled = true;
                    countdown.style.visibility = "hidden";
                    slider_A.disabled = true;
                    cardA.style.color = "#6c757d";
                }
            }, 1000);
        }, Delay);
    }, Intro);
}


/* dynamically changing the minimum values for the form fields A */
num_x_belief_A.onchange = function () {
    num_x_belief_A.reportValidity();
 }


/* script for the right hand side - fields B */
NextButton1.onclick = function () {

    // reset count down
    clearTimeout(countdown1);
    count.innerHTML = AnswerTime / 1000;

    NextButton1.style.display = "none";
    countdown.style.visibility = "hidden";
    num_x_belief_A.disabled = true;
    slider_A.disabled = true;

    cardC.style.color = "black";
    var i;
    for (i = 0; i < donations.length; i++) {
        donations[i].disabled = false;
    }
    SubmitButton.style.display = "block";

}


/* count the number of times page has been refreshed */
window.addEventListener("unload", function(){
    let count = parseInt(localStorage.getItem('counter') || 0);
    localStorage.setItem('counter', ++count)
    console.log("page was unloaded",localStorage.getItem('counter'), "times")
}, false);


/* dynamically determine confidence intervals to be displayed around belief A and belief B */
function changeCIA(val) {
    CIA.style.visibility = "visible";
    belief = Number(num_x_belief_A.value);
    let a = belief - 5 - (10 * (20 - val));
    let b = belief + 5 + (10 * (20 - val));
    if (a < 0) {
        document.getElementById("min_A").innerHTML = 0;
    } else {
        document.getElementById("min_A").innerHTML = a;
    }
    if (b > 400) {
        document.getElementById("max_A").innerHTML = 400;
    } else {
        document.getElementById("max_A").innerHTML = b;
    }
}


/* on form submission enable all fields again */
SubmitButton.onclick = function () {
    let loadcount = parseInt(localStorage.getItem('counter') || 0);
    console.log("page_loaded counter is", loadcount);

    if (loadcount > 0) {
        page_loaded.value = loadcount
    } else if (loadcount === null) {
        page_loaded.value = 0
    };
    localStorage.removeItem('counter');

    //Extract Each Element Value i.e. each form field
    for (let i = 0; i < form.elements.length; i++) {
        // enables each field
        form.elements[i].disabled = false;
    }
}


