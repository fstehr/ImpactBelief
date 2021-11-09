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
let num_x_belief_min_A = document.getElementById("num_x_belief_min_A");
let num_x_belief_max_A = document.getElementById("num_x_belief_max_A");

let cardB = document.getElementById("cardB");
let matrix2_white = document.getElementById('matrix2_white');
let matrix2 = document.getElementById('matrix2');
let num_x_belief_B = document.getElementById("num_x_belief_B");
let num_x_belief_min_B = document.getElementById("num_x_belief_min_B");
let num_x_belief_max_B = document.getElementById("num_x_belief_max_B");

let NextButton = document.getElementById("NextButton");

function HideImageLoadForm() {
    /* define protocol in seconds */
    setTimeout(function(){
        alert.style.display="none";
        matrix1_white.style.display="none";
        matrix1.style.display="block";
    },Intro);

    setTimeout(function(){
        matrix1.style.display="none";
        matrix1_white.style.display="block";
        cardA.style.color = "black";
        num_x_belief_A.disabled = false;
        num_x_belief_min_A.disabled = false;
        num_x_belief_max_A.disabled = false;

        // display count down
        countdown.style.display="block";
        // set counter for count down
        var counter = AnswerTime/1000;
        setInterval(function() {
            counter--;
            if (counter >= 0) {
                span = document.getElementById("count");
                span.innerHTML = counter;
            }
            if (counter === 0) {
                // alert('Please enter your estimate!');
                clearInterval(counter);
            }

        }, 1000);

    }, Intro+Delay);

    setTimeout(function(){
        num_x_belief_A.disabled = true;
        num_x_belief_min_A.disabled = true;
        num_x_belief_max_A.disabled = true;
        matrix2_white.style.display="none";
        countdown.style.display="none";
        matrix2.style.display="block";
        cardA.style.color = "#6c757d";
    }, Intro+Delay+AnswerTime);

    setTimeout(function(){
        matrix2_white.style.display="block";
        matrix2.style.display="none";
        cardB.style.color = "black";
        num_x_belief_B.disabled = false;
        num_x_belief_min_B.disabled = false;
        num_x_belief_max_B.disabled = false;

        // display count down
        countdown.style.display="block";
        // set counter for count down
        var counter = AnswerTime/1000;
        setInterval(function() {
            counter--;
            if (counter >= 0) {
                span = document.getElementById("count");
                span.innerHTML = counter;
            }
            if (counter === 0) {
                clearInterval(counter);
            }
        }, 1000);

        NextButton.style.display = "block";

    }, Intro+Delay+AnswerTime+Delay);

    setTimeout(function(){
        cardB.style.color = "#6c757d";
        num_x_belief_B.disabled = true;
        num_x_belief_min_B.disabled = true;
        num_x_belief_max_B.disabled = true;
    }, Intro+Delay+AnswerTime+Delay+AnswerTime);
}

/* on form submission enable all fields again */
function resetFields() {
    //Extract Each Element Value i.e. each form field
    for (let i = 0; i < form.elements.length; i++) {
        // enables each field
        form.elements[i].disabled = false;
    }
}


/* dynamically changing the minimum values for the form fields A */
num_x_belief_A.onchange = function () {
    num_x_belief_A.reportValidity();
    /* maximum of minA must be < belief */
    num_x_belief_min_A.setAttribute("max", this.value);
    /* minimum of maxA must be > belief */
    num_x_belief_max_A.setAttribute("min", this.value);
}

/* dynamically show error messages */
num_x_belief_min_A.onchange = function () {
    num_x_belief_min_A.reportValidity();
}
num_x_belief_max_A.onchange = function () {
    num_x_belief_max_A.reportValidity();
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
