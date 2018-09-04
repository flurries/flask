function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
                window.location.href = '/user/my/';
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 提交图片的post

$(document).ready(function () {
    $('#form-avatar').submit(function (e) {
        // 取消刷新
        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/user/profile/',
            dataType:'json',
            type: 'PATCH',
            success:function (data) {
                if(data.code == '200'){
                    $('#user-avatar').attr('src', '/static/media/' + data.img_avatar)

                }
            }
        })
    })
})


// 修改用户名
$(document).ready(function () {
    $('#form-name').submit(function (e) {
        // 取消刷新

        e.preventDefault()
        $(this).ajaxSubmit({
            url: '/user/profile_name/',
            dataType:'json',
            type: 'PATCH',
            success:function (data) {
                if(data.code == '1010'){
                    $('.error-msg').css("display","block");
                }else if(data.code == '200'){
                    $('.popup_con').css("display","block");
                    showSuccessMsg()
                }
            }
        })
    })
})