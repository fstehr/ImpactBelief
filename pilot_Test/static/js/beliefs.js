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
let num_x_belief_A = document.getElementById("num_x_belief_A");
let slider_A = document.getElementById("certainty_A")
let count = document.getElementById("count");

let cardB = document.getElementById("cardB");
let matrix2_white = document.getElementById('matrix2_white');
let matrix2 = document.getElementById('matrix2');
let num_x_belief_B = document.getElementById("num_x_belief_B");
let num_x_belief_min_B = document.getElementById("num_x_belief_min_B");
let num_x_belief_max_B = document.getElementById("num_x_belief_max_B");

let NextButton = document.getElementById("NextButton");
let SubmitButton = document.getElementById("SubmitButton");

let countdown1;

// Function that starts timing on page load (for Panel A)
function HideImageLoadForm() {
    console.log("page was loaded", localStorage.getItem('counter'), "times")

    /* define protocol in seconds */
    // Intro time delay to display matrix A
    setTimeout(function () {
        alert.style.display = "none";
        matrix1_white.style.display = "none";
        matrix1.style.display = "block";

        // after intro show hide matrix after 'Delay' seconds
        setTimeout(function () {
            matrix1.style.display = "none";
            matrix1_white.style.display = "block";
            cardA.style.color = "black";
            num_x_belief_A.disabled = false;
            slider_A.disabled = false;
            NextButton.style.display = "block";

            // display count down
            countdown.style.display = "block";
            // set counter for count down equal to answer time secs
            var counter = AnswerTime / 1000;
            setTimeout(function run() {
                counter--;
                console.log("countdown 1:", counter)
                if (counter >= 0) {
                    count.innerHTML = counter;
                    countdown1 = setTimeout(run, 1000);
                }
                if (counter === 0) {
                    // when countdown is run out disable fields
                    num_x_belief_A.disabled = true;
                    countdown.style.display = "none";
                    cardA.style.color = "#6c757d";
                }
            }, 1000);
        }, Delay);
    }, Intro);
}



/* dynamically changing the minimum values for the form fields A */
num_x_belief_A.onchange = function () {
    num_x_belief_A.reportValidity();
    document.getElementById("min_A").innerHTML = Number(num_x_belief_A.value) - 5;
    document.getElementById("max_A").innerHTML = Number(num_x_belief_A.value) + 5;
}

NextButton.onclick = function () {

    // reset count down
    clearTimeout(countdown1);
    count.innerHTML = AnswerTime / 1000;

    NextButton.style.display = "none";
    num_x_belief_A.disabled = true;
    matrix2_white.style.display="none";
    countdown.style.display="none";
    matrix2.style.display="block";
    cardA.style.color = "#6c757d";

    setTimeout(function(){
        matrix2_white.style.display="block";
        matrix2.style.display="none";
        cardB.style.color = "black";
        num_x_belief_B.disabled = false;
        num_x_belief_min_B.disabled = false;
        num_x_belief_max_B.disabled = false;
        SubmitButton.style.display = "block";

        // display count down
        countdown.style.display="block";
        // set counter for count down equal to answer time secs
        var counter = AnswerTime / 1000;
             setTimeout(function run() {
                counter--;
                if (counter >= 0) {
                    count.innerHTML = counter;
                    console.log("countdown 2:", counter)
                    setTimeout(run, 1000);
                }
                if (counter === 0) {
                    console.log("disable")
                    // when countdown is run out disable fields
                    num_x_belief_B.disabled = true;
                    num_x_belief_min_B.disabled = true;
                    num_x_belief_max_B.disabled = true;
                    countdown.style.display = "none";
                    cardB.style.color = "#6c757d";
                }
            }, 1000);
    }, Delay);
}

/* dynamically changing the minimum values for the form fields B */
num_x_belief_B.onchange = function () {
    num_x_belief_B.reportValidity();
    /* maximum of minA must be < belief */
    num_x_belief_min_B.setAttribute("max", this.value);
    /* minimum of maxA must be > belief */
    num_x_belief_max_B.setAttribute("min", this.value);
}

/* dynamically show error messages */
num_x_belief_min_B.onchange = function () {
    num_x_belief_min_B.reportValidity();
}
num_x_belief_max_B.onchange = function () {
    num_x_belief_max_B.reportValidity();
}


/* count the number of times page has been refreshed */
window.addEventListener("unload", function(){
    let count = parseInt(localStorage.getItem('counter') || 0);
    localStorage.setItem('counter', ++count)
    console.log("page was unloaded",localStorage.getItem('counter'), "times")
}, false);


function changeCI (val) {
    belief = Number(num_x_belief_A.value)
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
    //Extract Each Element Value i.e. each form field
    for (let i = 0; i < form.elements.length; i++) {
        // enables each field
        form.elements[i].disabled = false;
    }
    let page_loaded = document.getElementById("page_loaded")
    page_loaded.value = localStorage.getItem('counter')
    localStorage.removeItem('counter')
}


