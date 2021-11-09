let Intro = js_vars.sec_intro * 1000;
let Delay = js_vars.sec_per_matrix * 1000;
let AnswerTime = js_vars.sec_to_answer * 1000;
console.log("answer time is", AnswerTime);


function HideImageLoadForm() {
    var alert = document.getElementById('alert');
    var matrix1_white = document.getElementById('matrix1_white');
    var matrix1 = document.getElementById('matrix1');
    var num_x_belief_A = document.getElementById("num_x_belief_A");
    var num_x_belief_min_A = document.getElementById("num_x_belief_min_A");
    var num_x_belief_max_A = document.getElementById("num_x_belief_max_A");
    var num_x_belief_B = document.getElementById("num_x_belief_B");
    var num_x_belief_min_B = document.getElementById("num_x_belief_min_B");
    var num_x_belief_max_B = document.getElementById("num_x_belief_max_B");
    var cardA = document.getElementById("cardA");
    var cardB = document.getElementById("cardB");


    /* initially disable all fields */
    num_x_belief_A.disabled = true;
    num_x_belief_min_A.disabled = true;
    num_x_belief_max_A.disabled = true;
    num_x_belief_B.disabled = true;
    num_x_belief_min_B.disabled = true;
    num_x_belief_max_B.disabled = true;


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
    document.getElementById('num_x_belief_A').disabled = false;
    document.getElementById("num_x_belief_min_A").disabled = false;
    document.getElementById("num_x_belief_max_A").disabled = false;
    document.getElementById('num_x_belief_B').disabled = false;
    document.getElementById("num_x_belief_min_B").disabled = false;
    document.getElementById("num_x_belief_max_B").disabled = false;
}


/* dynamically changing the minimum values for the form fields A */
document.getElementById("num_x_belief_A").onchange = function () {
    /* maximum of minA must be < belief */
    var input = document.getElementById("num_x_belief_min_A");
    input.setAttribute("max", this.value);
    /* minimum of maxA must be > belief */
    var input2 = document.getElementById("num_x_belief_max_A");
    input2.setAttribute("min", this.value);
}
/* dynamically changing the minimum values for the form fields B */
document.getElementById("num_x_belief_B").onchange = function () {
    /* maximum of minA must be < belief */
    var input = document.getElementById("num_x_belief_min_B");
    input.setAttribute("max", this.value);
    /* minimum of maxA must be > belief */
    var input2 = document.getElementById("num_x_belief_max_B");
    input2.setAttribute("min", this.value);
}
