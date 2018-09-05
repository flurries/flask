function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function(){
    $.get('/house/area_facility/',function(data){
        if (data.code == '200'){
            for(var i=0;i<data.area_info.length;i++){
                var optipn_str = '<option value="'+ data.area_info[i].id +'">'+data.area_info[i].name+'</option>'
                $('#area-id').append(optipn_str)
            }

            for(var j=0; j<data.facilities_info.length ; j++){

                var facility_sty = '<li><div class="checkbox"><label>'
                facility_sty += '<input type="checkbox" name="facility" value="'+data.facilities_info[j].id+'">'+data.facilities_info[j].name
                facility_sty += '</label></div></li>'
                $('.house-facility-list').append(facility_sty)

            }
        }


    })
})


$(document).ready(function(){
    $('#form-house-info').submit(function (e) {
        e.preventDefault()
        $(this).ajaxSubmit({
            url:'/house/newhouse/',
            dataType:'json',
            type:'POST',
            success:function (data) {
                console.log(data)
                if(data.code=='200') {
                    $('#form-house-image').show()
                    $('#form-house-info').hide()
                    $('#house-id').val(data.house_id)
                }

            }
        })
    })
})

$(document).ready(function(){
    $('#form-house-image').submit(function (e) {
        e.preventDefault()
        $(this).ajaxSubmit({
            url:'/house/newhouse_img/',
            success:function (data) {
                console.log(data)
                if(data.code=='200') {
                    var img_str = ' <img style="height: 50px; width: 50px;" src="/static/media/'+ data.image_url +'" >'
                      $('.house-image-cons').append(img_str)
                }
            }
        })
    })
})
