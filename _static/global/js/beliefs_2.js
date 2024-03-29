let form = document.getElementById("form");
let treatment = js_vars.treatment;
let page_loaded = document.getElementById("page_loaded");


// call time variables from python
let Intro = js_vars.sec_intro * 1000;
let Delay = js_vars.sec_per_matrix * 1000;
let AnswerTime = js_vars.sec_to_answer * 1000;

// call all elements on the page
let alert = document.getElementById('alert');
let countdown = document.getElementById("countdown");

// card A
let cardA = document.getElementById("cardA");
let matrix1_white = document.getElementById('matrix1_white');
let matrix1 = document.getElementById('matrix1');
let beliefA = document.getElementById("beliefA");
let num_x_belief_A = document.getElementById("num_x_belief_A");
let slider_A = document.getElementById("certainty_A");
let CIA = document.getElementById("CIA");
let count = document.getElementById("count");

// card B
let cardB = document.getElementById("cardB");
let matrix2_white = document.getElementById('matrix2_white');
let matrix2 = document.getElementById('matrix2');
let beliefB = document.getElementById("beliefB");
let num_x_belief_B = document.getElementById("num_x_belief_B");
let slider_B = document.getElementById("certainty_B");
let CIB = document.getElementById("CIB");

// card C
let cardC = document.getElementById("cardC");
let donations = document.querySelectorAll("input[type=radio]");

// buttons
let NextButton1 = document.getElementById("NextButton1");
let NextButton2 = document.getElementById("NextButton2");
let NextButton3 = document.getElementById("NextButton3");
let SubmitButtonExA = document.getElementById("SubmitButtonExA");
let SubmitButtonExP = document.getElementById("SubmitButtonExP");



// Function that starts timing on page load (for Panel A)
function HideImageLoadForm() {
    console.log("page was loaded", localStorage.getItem('counter'), "times")
    alert.style.display = "block";
    /* on load disable donation fields */
    var i;
    for (i = 0; i < donations.length; i++) {
        donations[i].disabled = true;
    }
    if (treatment === "ExAnte" || treatment === "Spectator") {
        start_with_A_ExA();
    }
    else if (treatment === "ExPost") {
        start_with_A_ExP();
    }

}

function start_with_A_ExA() {
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
            NextButton1.style.visibility = "visible";

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
                    NextButton1.onclick = function () {
                        if(num_x_belief_A.value === "") {
                            window.alert("Please enter your estimate for the number  of pills");
                            return false;
                        }
                        else if(slider_A.className === "slider2"){
                            window.alert("Please enter how certain you are about your estimate");
                            return false;
                        }
                        else
                            continue_with_B();
                    }
                }
                if (counter === 0) {
                    // when countdown is run out disable fields
                    num_x_belief_A.disabled = true;
                    countdown.style.visibility = "hidden";
                    slider_A.disabled = true;
                    cardA.style.color = "#6c757d";
                    NextButton1.onclick = continue_with_B;
                }
            }, 1000);
        }, Delay);
    }, Intro);
}


/* script for the right hand side - fields B */
function continue_with_B() {
    // reset count down
    clearTimeout(countdown1);
    count.innerHTML = AnswerTime / 1000;

    NextButton1.style.visibility = "hidden";
    num_x_belief_A.disabled = true;
    slider_A.disabled = true;
    matrix2_white.style.display="none";
    countdown.style.visibility="hidden";
    matrix2.style.display="block";
    cardA.style.color = "#6c757d";

    setTimeout(function(){
        matrix2.style.display="none";
        // matrix2_white.style.display="block";
        beliefB.style.display = "block";
        cardB.style.color = "black";
        num_x_belief_B.disabled = false;
        slider_B.disabled = false;
        NextButton2.style.visibility = "visible";

        // display count down
        countdown.style.visibility="visible";
        // set counter for count down equal to answer time secs
        var counter = AnswerTime / 1000;
             setTimeout(function run() {
                counter--;
                if (counter >= 0) {
                    count.innerHTML = counter;
                    // console.log("countdown 2:", counter)
                    setTimeout(run, 1000);
                    NextButton2.onclick = function () {
                        if(num_x_belief_B.value === "") {
                            window.alert("Please enter your estimate for the number  of pills");
                            return false;
                        }
                        else if(slider_B.className === "slider2"){
                            window.alert("Please enter how certain you are about your estimate");
                            return false;
                        }
                        else
                            continue_with_donation();
                    }
                }
                if (counter === 0) {
                    console.log("disable")
                    // when countdown is run out disable fields
                    num_x_belief_B.disabled = true;
                    slider_B.disabled = true;
                    countdown.style.visibility = "hidden";
                    cardB.style.color = "#6c757d";
                    NextButton2.onclick = continue_with_donation;
                }
            }, 1000);
    }, Delay);
}

function continue_with_donation () {
    num_x_belief_B.disabled = true;
    slider_B.disabled = true;
    countdown.style.visibility = "hidden";
    cardB.style.color = "#6c757d";

    cardC.style.color = "black";
    var i;
    for (i = 0; i < donations.length; i++) {
        donations[i].disabled = false;
    }
    NextButton2.style.visibility = "hidden";
    SubmitButtonExA.style.visibility = "visible";
    SubmitButtonExA.onclick = submission_check;
}


function start_with_A_ExP() {
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
            NextButton1.style.visibility = "visible";
            NextButton1.onclick = continue_with_B_ExP;
        }, Delay);
    }, Intro);
}


/* script for the right hand side - fields B */
function continue_with_B_ExP() {

    NextButton1.style.visibility = "hidden";
    matrix2_white.style.display="none";
    matrix2.style.display="block";
    cardA.style.color = "#6c757d";

    setTimeout(function(){
        matrix2.style.display = "none";
        matrix2_white.style.display = "block";
        NextButton2.style.visibility = "visible";
        NextButton2.onclick = continue_with_donation_ExP;
    }, Delay);
}

function continue_with_donation_ExP () {
    cardC.style.color = "black";
    var i;
    for (i = 0; i < donations.length; i++) {
        donations[i].disabled = false;
    }
    NextButton2.style.visibility = "hidden";
    NextButton3.style.visibility = "visible";
    NextButton3.onclick = function () {
        var fields_clicked = 0;
        for(i = 0; i < donations.length; i++) {
            if(donations[i].checked){
                    ++fields_clicked
            }
        }
        //console.log("fields filled", fields_clicked)
        if (fields_clicked < 2) {
             window.alert("Please enter your donation decision for both projects");
             return false;
        }
        else if (fields_clicked === 2) {
            continue_with_belief_A_ExP();
        }
    }
}

function continue_with_belief_A_ExP () {
    cardC.style.color = "#6c757d";
    var i;
    for (i = 0; i < donations.length; i++) {
        donations[i].disabled = true;
    }
    NextButton3.style.visibility = "hidden";

    matrix1.style.display = "none";
    matrix1_white.style.display = "none";
    beliefA.style.display = "block";
    cardA.style.color = "black";
    num_x_belief_A.disabled = false;
    slider_A.disabled = false;
    NextButton1.style.visibility = "visible";

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
            NextButton1.onclick = function () {
                if(num_x_belief_A.value === "") {
                    window.alert("Please enter your estimate for the number  of pills");
                    return false;
                }
                else if(slider_A.className === "slider2"){
                    window.alert("Please enter how certain you are about your estimate");
                    return false;
                }
                else
                    continue_with_belief_B_ExP();
            }
        }
        if (counter === 0) {
            // when countdown is run out disable fields
            num_x_belief_A.disabled = true;
            countdown.style.visibility = "hidden";
            slider_A.disabled = true;
            cardA.style.color = "#6c757d";
            NextButton1.onclick = continue_with_belief_B_ExP;
        }
    }, 1000);
}


function continue_with_belief_B_ExP() {
    // reset count down
    clearTimeout(countdown1);
    count.innerHTML = AnswerTime / 1000;

    NextButton1.style.visibility = "hidden";
    num_x_belief_A.disabled = true;
    slider_A.disabled = true;
    cardA.style.color = "#6c757d";

    matrix2_white.style.display="none";
    beliefB.style.display = "block";
    cardB.style.color = "black";
    num_x_belief_B.disabled = false;
    slider_B.disabled = false;
    NextButton2.style.display = "none";
    SubmitButtonExP.style.display = "inline";

    // display count down
    countdown.style.visibility="visible";
    // set counter for count down equal to answer time secs
    var counter = AnswerTime / 1000;
         setTimeout(function run() {
            counter--;
            if (counter >= 0) {
                count.innerHTML = counter;
                // console.log("countdown 2:", counter)
                setTimeout(run, 1000);
                SubmitButtonExP.onclick = function () {
                    if(num_x_belief_B.value === "") {
                        window.alert("Please enter your estimate for the number  of pills");
                        return false;
                    }
                    else if(slider_B.className === "slider2"){
                        window.alert("Please enter how certain you are about your estimate");
                        return false;
                    }
                    else
                        submission_check();
                }
            }
            if (counter === 0) {
                console.log("disable")
                // when countdown is run out disable fields
                num_x_belief_B.disabled = true;
                slider_B.disabled = true;
                countdown.style.visibility = "hidden";
                cardB.style.color = "#6c757d";
                SubmitButtonExP.onclick = submission_check;
            }
        }, 1000);
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

function changeCIB(val) {
    CIB.style.visibility = "visible";
    belief = Number(num_x_belief_B.value);
    let a = belief - 5 - (10 * (20 - val));
    let b = belief + 5 + (10 * (20 - val));
    if (a < 0) {
        document.getElementById("min_B").innerHTML = 0;
    } else {
        document.getElementById("min_B").innerHTML = a;
    }
    if (b > 400) {
        document.getElementById("max_B").innerHTML = 400;
    } else {
        document.getElementById("max_B").innerHTML = b;
    }
}


/* on form submission enable all fields again */
function submission_check () {
    let loadcount = parseInt(localStorage.getItem('counter') || 0);
    console.log("page_loaded counter is", loadcount);

    if (loadcount > 0) {
        page_loaded.value = loadcount;
    } else if (loadcount === null) {
        page_loaded.value = 0;
    }
    localStorage.removeItem('counter');

    //Extract Each Element Value i.e. each form field
    for (let i = 0; i < form.elements.length; i++) {
        // enables each field
        form.elements[i].disabled = false;
    }
}
