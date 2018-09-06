function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var search_url = location.search
    house_id = search_url.split('=')[1]
    $.get('/house/detail/'+house_id+'/',function (data) {
        console.log(data)
        var booking_temp = template('booking_tem_script', {ohouse: data.house_detail})
        $('.house-info').html(booking_temp)
    })

    var start_date = $('#start-date').val()
    var end_date = $('#end-date').val()
    $('.submit-btn').click(function () {
        var start_date = $('#start-date').val()
        var end_date = $('#end-date').val()
        $.post('/order/order/',{'begin_date': start_date, 'end_date': end_date, 'house_id': house_id},function (data) {
        if(data.code == '200'){
            location.href = '/order/orders/'
        }
        })

    })
})



















