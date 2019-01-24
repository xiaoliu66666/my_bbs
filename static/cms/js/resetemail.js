$(function () {
    $('#captcha-btn').click(function (event) {
        event.preventDefault();
        var email = $("input[name=email]").val();
        if (!email) {
            bbsalert.alertInfoToast("请输入邮箱！");
            return;
        }

        bbsajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] === 200){
                    bbsalert.alertSuccessToast(data['message']);
                }else{
                    bbsalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                bbsalert.alertNetworkError();
            }
        })
    })
});
