let Intro = 3 * 1000;
let Delay = js_vars.sec_per_matrix * 1000;
let timeoutcount = 0;

function HideImageLoadForm() {
    setTimeout(function(){
        document.getElementById('alert').style.display="none"
        document.getElementById('matrix1').style.display="block"
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
                /*document.getElementById('field1').value = 0;
                console.log("Field 1 is", document.getElementById('field1').value);
                timeoutcount++;
                console.log("timeoutcount:", timeoutcount.value);
                Show_next_form1(); */
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
            // set timer
            var counter = 15;
            setInterval(function() {
                counter--;                  // this operand subtracts 1 and returns new value
                if (counter >= 0) {
                    span = document.getElementById("count");
                    span.innerHTML = counter;
                }
                if (counter === 0) {
                    //alert('Please enter your estimate!');
                    clearInterval(counter);
                   /* document.getElementById('field2').value = 0;
                    console.log("Field 2 is", document.getElementById('field2').value);
                    timeoutcount++;
                    console.log("timeoutcount:", timeoutcount)
                    Show_next_form2(); */
                }
            }, 1000);   // timeout 1000 defines steps to be seconds

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
            counter--;   // this operand subtracts 1 and returns new value
            if (counter >= 0) {
                span = document.getElementById("count");
                span.innerHTML = counter;
            }
            if (counter === 0) {
                // alert('Please enter your estimate!');
                clearInterval(counter);
               /* field3 = document.getElementById('field3');
                field3.value = 0;
                console.log("Field 3 is", field3.value)
                timeoutcount++;
                document.getElementById('timeoutcount').value = timeoutcount;
                console.log("timeoutcount:", timeoutcount)
                document.getElementById("form").submit(); */
            }
        }, 1000);  // timeout 1000 defines steps to be seconds

        document.getElementById('matrix3').style.display="none"
        document.getElementById('time-alert').style.display="block"
        document.getElementById('Question').style.display="block"
        document.getElementById('field3').style.display="block"
        document.getElementById('btn-submit').style.display="block"
    }, Delay+Intro);
}
