//https://www.hongkiat.com/blog/on-click-animated-gif/

(function($) {

  // Get the .gif images from the "data-alt".
	var getGif = function() {
		var gif = [];
		$('img').each(function() {
			var data = $(this).data('alt');
			gif.push(data);
		});
		return gif;
	}


	// Preload all the gif images.
	//var gif = getGif();
	//var image = [];

	//$.each(gif, function(index) {
	//	image[index]     = new Image;
	//	image[index].src = gif[index];
	//});

	// Change the image to .gif when clicked and vice versa.
	$('figure').on('click', function() {
		// set variable gif clicked
		var touch_element = document.getElementById("gif_click");
    	touch_element.value = "True";
    	sessionStorage.setItem("gif_click", "True");
    	console.log("local storage gif clicked:", sessionStorage.getItem('gif_click'))



		var $this   = $(this),
				$index  = $this.index(),
				$img    = $this.children('img'),
				$imgSrc = $img.attr('src'),
				$imgAlt = $img.attr('data-alt'),
				$imgExt = $imgAlt.split('.');
				
		if($imgExt[1] === 'gif') {
			$img.attr('src', $img.data('alt')).attr('data-alt', $imgSrc);
		} else {
			$img.attr('src', $imgAlt).attr('data-alt', $img.data('alt'));
		}
	});

})(jQuery);


// SET HIDDEN FORM FIELDS
function set_clicked() {
	let touch_element = document.getElementById("equation_click");
	touch_element.value = "True";
	sessionStorage.setItem("eq_click", "True");
	console.log("local storage eq click:", sessionStorage.getItem('eq_click'));
}

$(document).ready(function () {
	// get var values from local storage
	let early_click = sessionStorage.getItem("early_click");
	let eq_click = sessionStorage.getItem('eq_click');
	let gif_click = sessionStorage.getItem('gif_click');

	// set field values to value from local storage
	if (early_click !== null) $('#clicked_early').val(early_click);
	if (eq_click !== null) $('#equation_click').val(eq_click);
	if (gif_click !== null) $('#gif_click').val(gif_click);
});

// https://www.sitepoint.com/quick-tip-persist-checkbox-checked-state-after-page-reload/
// get change for check box
$("#checkbox-container :checkbox").on("change", function(){
  console.log("The checkbox with the ID '" + this.id + "' changed");
});

// set local storage var to checked if this happened
var checkboxValues = JSON.parse(sessionStorage.getItem('checkboxValues')) || {};
var $checkboxes = $("#checkbox-container :checkbox");

$checkboxes.on("change", function(){
  $checkboxes.each(function(){
    checkboxValues[this.id] = this.checked;
  });
  sessionStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));
});

// on page load set value of checkboxes accordingly
$.each(checkboxValues, function(key, value) {
  $("#" + key).prop('checked', value);
});

