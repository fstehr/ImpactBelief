//https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Timeouts_and_intervals


var start = new Date().getTime(),
    time = 0;

function instance()
{
    time += 100;
    var diff = (new Date().getTime() - start) - time;
    window.setTimeout(instance, (100 - diff));
}

window.setTimeout(instance, 100);

// If you've got a box that's supposed to slide onto the screen, expand downwards,
// then fade in its contents, don't try to make all three events separate with delays
// timed to make them fire one after another - use callbacks, so once the first event
// is done sliding it calls the expander, once that's done it calls the fader. jQuery
// can do it easily, and I'm sure other libraries can as well.
window.onload = function () {
    setTimeout(function() {
        $("#output").append(" one ");
       setTimeout(function() {
           $("#output").append(" two ");
       }, 100);
    }, 1000); //https://newbedev.com/execution-order-of-multiple-settimeout-functions-with-same-interval
}



// Common Mistake #9: Providing a string as the first argument to setTimeout or setInterval
// For starters, let’s be clear on something here: Providing a string as the first argument to setTimeout or setInterval is not itself a mistake per se. It is perfectly legitimate JavaScript code. The issue here is more one of performance and efficiency. What is rarely explained is that, under the hood, if you pass in a string as the first argument to setTimeout or setInterval, it will be passed to the function constructor to be converted into a new function. This process can be slow and inefficient, and is rarely necessary.
//
// The alternative to passing a string as the first argument to these methods is to instead pass in a function. Let’s take a look at an example.
//
// Here, then, would be a fairly typical use of setInterval and setTimeout, passing a string as the first parameter:
//
// setInterval("logTime()", 1000);
// setTimeout("logMessage('" + msgValue + "')", 1000);
// The better choice would be to pass in a function as the initial argument; e.g.:
//
// setInterval(logTime, 1000);   // passing the logTime function to setInterval
//
// setTimeout(function() {       // passing an anonymous function to setTimeout
//     logMessage(msgValue);     // (msgValue is still accessible in this scope)
//   }, 1000);





//global timeout references we can use to stop them
var timeouts = {};


//timer demo function with normal/self-adjusting argument
function timer(form, adjust, morework)
{
    //create the timer speed, a counter and a starting timestamp
    var speed = 50,
    counter = 0,
    start = new Date().getTime();

    //timer instance function
    function instance()
    {
        //if the morework flag is true
        //do some calculations to create more work
        if(morework)
        {
            for(var x=1, i=0; i<1000000; i++) { x *= (i + 1); }
        }

        //work out the real and ideal elapsed time
        var real = (counter * speed),
        ideal = (new Date().getTime() - start);

        //increment the counter
        counter++;

        //display the values
        form.ideal.value = real;
        form.real.value = ideal;

        //calculate and display the difference
        var diff = (ideal - real);
        form.diff.value = diff;

        //if the adjust flag is true
        //delete the difference from the speed of the next instance
        if(adjust)
        {
            timeouts[form.id] = window.setTimeout(function() { instance(); }, (speed - diff));
        }

        //otherwise keep the speed normal
        else
        {
            timeouts[form.id] = window.setTimeout(function() { instance(); }, speed);
        }
    };

    //now kick everything off with the first timer instance
    timeouts[form.id] = window.setTimeout(function() { instance(); }, speed);
}



//bind a submit handler to the self-adjusting form
document.getElementById('adjusting').onsubmit = function()
{
    //call the timerdemo function with both flags true
    timer(this, true, true);

    //cancel the normal submit
    return false;
};

//bind a reset handler to stop it
document.getElementById('adjusting').onreset = function()
{
    //stop the form's timer
    window.clearTimeout(timeouts[this.id]);

    //cancel the normal reset
    return false;
};




