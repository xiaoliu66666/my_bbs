$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this)
        var dialog = $("#banner-dialog");
        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");

        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();

        var submitType = self.attr('data-type');
        var bannerId = self.attr("data-id");

        if(!name || !image_url || !link_url || !priority){
             bbsalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }

        var url = '';
        if(submitType == 'update'){
            url = '/cms/ubanner/';
        }else{
            url = '/cms/abanner/';
        }

        bbsajax.post({
            "url": url,
            "data": {
                'name':name,
                'image_url': image_url,
                'link_url': link_url,
                'priority':priority,
                'banner_id': bannerId,
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
                     bbsalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                bbsalert.alertNetworkError();
            }

        });
    });
});


$(function () {
    $(".edit-banner-btn").click(function (event) {
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var image_url = tr.attr("data-image");
        var link_url = tr.attr("data-link");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imageInput = dialog.find("input[name='image_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save-banner-btn");


        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type", "update");
        saveBtn.attr("data-id", tr.attr("data-id"));

    });
});


$(function () {
    $(".delete-banner-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        bbsalert.alertConfirm({
            "msg":"您确定要删除这个轮播图吗？",
            'confirmCallback': function () {
                bbsajax.post({
                    'url': '/cms/dbanner/',
                    'data':{
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            bbsalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});


//上传图片，通过FileReader的readAsDataURL方法得到的是data-url
//但是数据太长无法存入数据库
//$(function () {
//    var inputBox = document.getElementById("upload-btn");
//    inputBox.addEventListener("change",function(){
//        var reader = new FileReader();
//        reader.readAsDataURL(inputBox.files[0]);//发起异步请求
//        reader.onload = function(){
//        //读取完成后，数据保存在对象的result属性中
//        var imageInput = $("input[name='image_url']");
//        imageInput.val(this.result);
//        console.log(this.result)
//
//        }
//    });
//});
