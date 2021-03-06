function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        $.ajax({
            url:'/user/my_login/',
            data:{'phone':mobile,'pwd':passwd},
            dataType:'json',
            type:'GET',
            success:function(data){
                console.log(data)
                if(data.code == '200'){
                    location.href = '/user/my/'
                }
                if(data.code == '1007'){
                    $('#mobile-err span').html(data.msg)
                    $('#mobile-err').show()
                }
            }
        })
    });
})