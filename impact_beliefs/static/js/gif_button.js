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

	var gif = getGif();

	// Preload all the gif images.
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