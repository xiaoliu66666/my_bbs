
$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var remember_input = $("input[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remember_input.checked ? 1 : 0;

        bbsajax.post({
            'url': '/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember,
            },
            'success': function (data) {
                if (data['code'] === 200){
                    //注册成功跳转到首页
                    var return_to = $('#return-to-span').text();
                    if (return_to){
                        window.location = return_to;
                    }else{
                        window.location = '/';
                    }
                }else{
                    bbsalert.alertInfo(data['message']);
                }
            }
        });
    });
})
