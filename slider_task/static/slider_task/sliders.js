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


$(function()
{
$('.slider').on('input change', function(){
    $(this).next($('.slider_label')).html(this.value);
     });
      $('.slider_label').each(function(){
          const value = $(this).prev().attr('value');
          $(this).html(value);
     });
})


 function myFunction() {
              var check_sliders = document.getElementById("check_sliders");
              var sliders = document.getElementsByClassName("slider");
              var num_centered = 0;
              var text;

                for (i = 0; i < sliders.length; i++) {
                    if ( sliders[i].value == 50) {
                        num_centered = num_centered + 1;
                    }
                }
                if (num_centered == sliders.length ) {
                    form.submit();
                    text = ""
                }
                else {
                    event.preventDefault();
                    window.scrollTo(0, 0);
                    document.getElementById('alert').style.display="block";
                }
                document.getElementById("errormessage").innerHTML = text;
            }


