$(function () {
    $('#captcha-img').click(function(event) {
        var self = $(this);
        var src = self.attr('src');
        var new_src = src + '?' + Math.random();
        self.attr('src', new_src);
    })
})
   
