$(function () {
    $('#captcha-img').click(function(event) {
        var self = $(this);
        var src = self.attr('src');
        var new_src = src + '?' + Math.random();
        self.attr('src', new_src);
    })
})

$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_input = $('input[name=telephone]');
        var username_input = $('input[name=username]');
        var password1_input = $('input[name=password1]');
        var password2_input = $('input[name=password2]');
        var graph_captcha_input = $('input[name=graph_captcha]');

        var telephone = telephone_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        bbsajax.post({
            'url': '/register/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function (data) {
                if (data['code'] === 200){
                    //注册成功跳转到首页
                    window.location = '/';
                }else{
                    bbsalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                bbsalert.alertNetworkError();
            }
        });
    });
})
