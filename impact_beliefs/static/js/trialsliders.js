let Intro = 10 * 1000;
let Delay = js_vars.sec_per_matrix * 1000;

function HideImageLoadForm() {
    setTimeout(function(){
        document.getElementById('alert').style.display="none"
        document.getElementById('matrix').style.display="block"
    },Intro);
    setTimeout(function(){
        // set counter for count down
        var counter = 15;
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

        document.getElementById('matrix').style.display="none"
        document.getElementById('time-alert').style.display="block"
        document.getElementById('Question').style.display="block"
        document.getElementById('field').style.display="block"
        document.getElementById('btn-submit').style.display="block"

    }, Delay+Intro);
}
