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


// for now define it based on element being zero; change later using event listener & set touched function
function checkTouched() {
              var sliders = document.getElementsByClassName("slider");
              var num_touched = 0;

                for (i = 0; i < sliders.length; i++) {
                    if (sliders[i].value != 0) {
                        num_touched = num_touched + 1;
                    }
                }
                if (num_touched == sliders.length ) {
                      form.submit();
                }
                else {
                    event.preventDefault();
                    window.scrollTo(0, 0)
                    document.getElementById('alert').style.display="block";
                }
            }


            /*
            function set_touched(event) {
                var hidden_field_id = this.id.substring(0, this.id.length-7) + "touched";
                var touch_element = document.getElementById(hidden_field_id);
                touch_element.value = "True";
                this.removeEventListener('change', set_touched)
                }

            var sliders = document.getElementsByClassName("slider");
                for (i = 0; i < sliders.length; i++) {
                    sliders[i].addEventListener('change', set_touched);
                }
             */
