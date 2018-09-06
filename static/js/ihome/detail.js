function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    var search_url = location.search
    house_id = search_url.split('=')[1]
    $.get('/house/detail/'+house_id+'/',function (data) {
        console.log(data)
        if (data.code == '200'){
            var li = ''
            for (var i = 0; i < data.house_detail.images.length; i++ ){
                li +='<li class="swiper-slide"><img src="/static/media/'+ data.house_detail.images[i] +'"></li>'
            }
            $('.swiper-wrapper').append(li)
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay:2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })

            $('.house-price span').html(data.house_detail.price)
            $('.house-title').html(data.house_detail.title)
            var user_avatar = '<img src="/static/media/'+ data.house_detail.user_avatar +'">'
            $('.landlord-pic').append(user_avatar)
            $('.landlord-name span').html(data.house_detail.user_name)
            $('.text-center li').html(data.house_detail.address)
            $('.icon-text1').append('<h3>出租'+ data.house_detail.room_count +'间</h3>')
            $('.icon-text1').append('<p>房屋面积:'+ data.house_detail.acreage +'</p>')
            $('.icon-text1').append('<p>房屋户型:'+ data.house_detail.unit +'</p>')
            $('.icon-text2').append('<h3>宜住'+data.house_detail.capacity+'人</h3>')
            $('.icon-text3').append(' <p>'+data.house_detail.beds+'</p>')
            $('.house-info-list:last').append('<li>收取押金<span>'+ data.house_detail.deposit +'</span></li>')
            $('.house-info-list:last').append('<li>最少入住天数<span>'+ data.house_detail.min_days +'</span></li>')
            $('.house-info-list:last').append('<li>最多入住天数<span>'+ data.house_detail.max_days +'</span></li>')
            var clearfi = ''
            for (var j = 0; j < data.house_detail.facilities.length; j++ ){
                clearfi += '<li><span class="'+ data.house_detail.facilities[j].css +'"></span>'+ data.house_detail.facilities[j].name +'</li>'
            }
            $('.clearfix').append(clearfi)
            $('.book-house').attr('href', '/house/booking/?house_id=' + house_id)
        }
    })
})
