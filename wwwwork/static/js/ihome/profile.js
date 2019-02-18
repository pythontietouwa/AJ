function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('#form-fix_avatar').submit(function (e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/fix_avatar/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                console.log(data)
                if(data.code == '200'){
                    alert('修改头像成功')
                    location.href = '/user/profile/'
                }
                if(data.code == '1001'){
                    $('#erro-msg span').html(data.msg);
                    $("#erro-msg").show();
                }
             },
            error:function(data){
                alert('请求失败了')
            }
        })
    })
    $('#form-fix_name').submit(function (e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/fix_name/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                console.log(data)
                if(data.code == '200'){
                    alert('修改用户名成功')
                    location.href = '/user/my/'
                };
                if(data.code == '3001'){
                    $('#erro-msg span').html(data.msg);
                    $("#erro-msg").show();
                };
             },
            error:function(data){
                alert('请求失败')
            }
        })
    })
})
