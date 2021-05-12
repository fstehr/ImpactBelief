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
                var sliders = document.getElementsByClassName("slider");
                if (touched == sliders.length ) {
                      form.submit();
                }
                else {
                    event.preventDefault();
                    window.scrollTo(0, 0)
                    document.getElementById('alert').style.display="block";
                }
            }


// define touched as counter with eventlistener on change
touched = 0

function set_touched(event) {
    touched += 1;
    // console.log("touched counter is", touched);
    this.removeEventListener('change', set_touched);
    }

var sliders = document.getElementsByClassName("slider");
    for (i = 0; i < sliders.length; i++) {
        sliders[i].addEventListener('change', set_touched);
    }

