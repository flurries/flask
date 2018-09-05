$(document).ready(function(){
    $(".auth-warn").show();
})


$(document).ready(function(e){
    $.get('/house/house_info/',function(data){
        if (data.code == '200'){
            $('.auth-warn').hide()
            $('#houses-list').show()
            for (var i = 0; i < data.house_info.length; i++) {
                var li = '<li><a href="/detail.html?id=&f=my">'
                li += '<div class="house-title"><h3>房屋ID:1 —— ' + data.house_info[i].title + '</h3>'
                li += '</div><div class="house-content">'
                li += '<img src="/static/media/' + data.house_info[i].image + '">'
                li += '<div class="house-text"><ul><li>位于:' + data.house_info[i].address + '</li>'
                li += '<li>价格：￥' + data.house_info[i].price + '/晚</li>'
                li += '<li>发布时间：' + data.house_info[i].create_time + '</li>'
                li += '</ul></div></div></a></li>'
                $('#houses-list').append(li)
            }
    }if(data.code == '1014'){
            $('.auth-warn').show()
            $('#houses-list').hide()
        }
    })
})


