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


document.getElementById("slieder").oninput = function() {
    myFunction()
};


function myFunction() {
   var val = document.getElementById("slider").value //gets the oninput value
   document.getElementById('output').innerHTML = val //displays this value to the html page
   console.log(val)
}