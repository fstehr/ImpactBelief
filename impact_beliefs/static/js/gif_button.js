var getGif = function() {
        var gif = [];
        $('img').each(function() {
                var data = $(this).data('alt');
                gif.push(data);
        });
        return gif;
}
var gif = getGif();