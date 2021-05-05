// Source: https://www.jqueryscript.net/other/bootstrap-tabs-carousel.html

function bootstrapTabControl(){
  var i, items = $('.back-and-forth'), pane = $('.tab-pane');

// NEXT -----
  $('.nexttab').on('click', function(){
      for(i = 0; i < items.length; i++){
          if($(items[i]).hasClass('active') == true){
              break;
          }
      }
      if(i < items.length - 1){
          // for tab
          $(items[i]).removeClass('active');
          $(items[i+1]).addClass('active');
          // for pane
          $(pane[i]).removeClass('show active');
          $(pane[i+1]).addClass('show active');
      }

  });

// PREV -----
  $('.prevtab').on('click', function(){
      for(i = 0; i < items.length; i++){
          if($(items[i]).hasClass('active') == true){
              break;
          }
      }
      if(i != 0){
          // for tab
          $(items[i]).removeClass('active');
          $(items[i-1]).addClass('active');
          // for pane
          $(pane[i]).removeClass('show active');
          $(pane[i-1]).addClass('show active');
      }
  });
}
bootstrapTabControl();


function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}