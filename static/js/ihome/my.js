function logout() {
    $.get("/user/logout/", function(data){
        if (data.code == '200') {
            location.href = "/user/login/";
        }
    })
}


$(document).ready(function(){
    $.get('/user/my_info/', function (data) {
        $('#user-name').html(data.user_info.name)
        $('#user-mobile').html(data.user_info.phone)
        $('#user-avatar').attr('src', data.user_info.avatar)
    })

})
$(document).ready(function(){

    $.get('/user/my_info/', function(data){
        if(data.code == '200'){
            $('#user-name').html(data.user_info.name)
            $('#user-mobile').html(data.user_info.phone)
            $('#user-avatar').attr('src', '/static/media/' + data.user_info.avatar)
        }
    })
})