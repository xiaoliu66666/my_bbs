$(function () {
    $('#submit').click(function (event) {
        //阻止按钮默认的提交表单行为
        event.preventDefault();
        var oldpwdE = $('input[name=oldpwd]');
        var newpwdE = $('input[name=newpwd]');
        var newpwd2E = $('input[name=newpwd2]');

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        //这里使用我们自己封装好的bbsajax，它具有了csrf
        bbsajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                //根据状态码判断
                if (data['code'] === 200){
                    //弹出成功的提示框，提示语是从后台传过来的message
                    bbsalert.alertSuccessToast(data['message']);
                    oldpwdE.val('');   //完成请求后把表单输入的值清空
                    newpwdE.val('');
                    newpwd2E.val('');
                }else{
                    bbsalert.alertError(data['message']);
                    oldpwdE.val('');
                    newpwdE.val('');
                    newpwd2E.val('');
                }
            },
            'fail': function (error) {
                bbsalert.alertNetworkError();
            }
        });
    });
})