function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
            window.location.href = '/user/my/'
        },1000) 
    });
}

$(document).ready(function () {
    $('#form-auth').submit(function (e) {
        e.preventDefault();
        $('#real-name').focus(function () {
             $('.error-msg').hide()
        })
        $('#id-card').focus(function () {
             $('.error-msg').hide()
        })

        var real_name = $('#real-name').val()
        var id_card = $('#id-card').val()
        $.ajax({
            url:'/user/auth/',
            dataType:'json',
            data:{'real_name':real_name, 'id_card':id_card},
            type:'PATCH',
            success:function (data) {
                if(data.code == '1012' | data.code == '1013'){
                    $('.error-msg').html(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '200'){
                    // $('.btn-success').hide()
                    showSuccessMsg()
                }
            }
        })
    })
})

function auth_info() {
    $.get('/user/auth_info/', function (data) {
    if(data.code == '200'){
        $('#real-name').val(data.user_info.id_name)
        $('#id-card').val(data.user_info.id_card)
        if(data.user_info.id_name){
            $('.btn-success').hide()
            $('#real-name').prop('readonly', true)
            $('#id-card').prop('readonly', true)

        }
    }
})
}

auth_info()