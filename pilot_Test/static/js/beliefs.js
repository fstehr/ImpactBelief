let Intro = js_vars.sec_intro * 1000;
let Delay = js_vars.sec_per_matrix * 1000;
let AnswerTime = js_vars.sec_to_answer * 1000;
console.log("answer time is", AnswerTime);

/* call all elements */
let alert = document.getElementById('alert');
let matrix1_white = document.getElementById('matrix1_white');
let matrix1 = document.getElementById('matrix1');
let num_x_belief_A = document.getElementById("num_x_belief_A");
let num_x_belief_min_A = document.getElementById("num_x_belief_min_A");
let num_x_belief_max_A = document.getElementById("num_x_belief_max_A");
let num_x_belief_B = document.getElementById("num_x_belief_B");
let num_x_belief_min_B = document.getElementById("num_x_belief_min_B");
let num_x_belief_max_B = document.getElementById("num_x_belief_max_B");
let cardA = document.getElementById("cardA");
let cardB = document.getElementById("cardB");


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
    }, Delay+Intro);

    setTimeout(function(){
        num_x_belief_A.disabled = true;
        num_x_belief_min_A.disabled = true;
        num_x_belief_max_A.disabled = true;
    }, Delay+Intro+AnswerTime);
}

function resetFields() {
    let form = document.getElementById("form");
    //Extract Each Element Value i.e. each form field
    for (let i = 0; i < form.elements.length; i++) {
        // enables each field
        form.elements[i].disabled = false;
    }
}


/* dynamically changing the minimum values for the form fields A */
    num_x_belief_A.onchange = function () {
    /* maximum of minA must be < belief */
    num_x_belief_min_A.setAttribute("max", this.value);
    /* minimum of maxA must be > belief */
    num_x_belief_max_A.setAttribute("min", this.value);
}
/* dynamically changing the minimum values for the form fields B */
    num_x_belief_B.onchange = function () {
    /* maximum of minA must be < belief */
    num_x_belief_min_B.setAttribute("max", this.value);
    /* minimum of maxA must be > belief */
    num_x_belief_max_B.setAttribute("min", this.value);
}
