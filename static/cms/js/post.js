$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uhpost/";
        }else{
            url = "/cms/hpost/";
        }
        bbsajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    bbsalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    bbsalert.alertInfo(data['message']);
                }
            }
        });
    });
});


$(function () {
    $(".delete-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");

        bbsajax.post({
            'url': "/cms/dpost/",
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    bbsalert.alertSuccessToast();
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    console.log(data['message'])
                    bbsalert.alertInfo(data['message']);
                }
            }
        });
    });
});