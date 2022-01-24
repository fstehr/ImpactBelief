// display current value next to slider
$(function()
{
$('.slider').on('input change', function(){
    $(this).next($('.slider_label')).html(this.value);
     });
      $('.slider_label').each(function(){
          var value = $(this).prev().attr('value');
        $(this).html(value);
     });
})




// on form submission, check that all elements have been moved
function checkTouched() {
    var sliders = document.getElementsByClassName("slider2");
    // console.log("length of sliders list in class slider 2", sliders.length)
    if (sliders.length === 0) {
          form.submit();
    }
    else {
        event.preventDefault();
        window.scrollTo(0, 0);
        document.getElementById('alert').style.display="block";
    }
}


// define touched as counter with eventlistener on change
touched = 0

function set_touched(event) {
    touched += 1;
    this.className = "slider";
    // console.log("touched counter is", touched);
    this.removeEventListener('mouseup', set_touched);
    }

var sliders = document.getElementsByClassName("slider2");
    for (i = 0; i < sliders.length; i++) {
        sliders[i].addEventListener('mouseup', set_touched);
    }
