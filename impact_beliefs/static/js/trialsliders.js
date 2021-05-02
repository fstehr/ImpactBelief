let Intro = 3 * 1000;
let Delay = js_vars.sec_per_matrix * 1000;

function HideImageLoadForm() {
    setTimeout(function(){
        document.getElementById('alert').style.display="none"
        document.getElementById('matrix1').style.display="block"
    },Intro);
    setTimeout(function(){
        var counter = 15;
        setInterval(function() {
            counter--;
            if (counter >= 0) {
                span = document.getElementById("count");
                span.innerHTML = counter;
            }
            if (counter === 0) {
                alert('Please enter your estimate!');
                clearInterval(counter);
            }
        }, 1000);

        document.getElementById('matrix1').style.display="none"
        document.getElementById('time-alert').style.display="block"
        document.getElementById('Question').style.display="block"
        document.getElementById('field1').style.display="block"
        document.getElementById('btn-nosubmit').style.display="block"

    }, Delay+Intro);
}

function Show_next_form1() {
    document.getElementById('time-alert').style.display="none"
    document.getElementById('Question').style.display="none"
    document.getElementById('field1').style.display="none"
    document.getElementById('btn-nosubmit').style.display="none"
    document.getElementById('alert').style.display="block"

    setTimeout(function(){
        document.getElementById('alert').style.display="none"
        document.getElementById('matrix2').style.display="block"
    },Intro);
    setTimeout(function(){
        var counter = 15;
        setInterval(function() {
            counter--;
            if (counter >= 0) {
                span = document.getElementById("count");
                span.innerHTML = counter;
            }
            if (counter === 0) {
                alert('Please enter your estimate!');
                clearInterval(counter);
            }
        }, 1000);

        document.getElementById('matrix2').style.display="none"
        document.getElementById('time-alert').style.display="block"
        document.getElementById('Question').style.display="block"
        document.getElementById('field2').style.display="block"
        document.getElementById('btn-nosubmit2').style.display="block"
    }, Delay+Intro);
}
function Show_next_form2() {
    document.getElementById('time-alert').style.display="none"
    document.getElementById('Question').style.display="none"
    document.getElementById('field2').style.display="none"
    document.getElementById('btn-nosubmit2').style.display="none"
    document.getElementById('alert').style.display="block"

    setTimeout(function(){
        document.getElementById('alert').style.display="none"
        document.getElementById('matrix3').style.display="block"
    },Intro);
    setTimeout(function(){
        var counter = 15;
        setInterval(function() {
            counter--;
            if (counter >= 0) {
                span = document.getElementById("count");
                span.innerHTML = counter;
            }
            if (counter === 0) {
                alert('Please enter your estimate!');
                clearInterval(counter);
            }
        }, 1000);

        document.getElementById('matrix3').style.display="none"
        document.getElementById('time-alert').style.display="block"
        document.getElementById('Question').style.display="block"
        document.getElementById('field3').style.display="block"
        document.getElementById('btn-submit').style.display="block"
    }, Delay+Intro);
}
