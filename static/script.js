function login(){
    let user_id = $("#user_id").val();
    let user_password = $("#user_password").val();
    $.ajax({
        type: "POST",
        url: "/login",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({"user_id" : user_id, "user_password" : user_password}),
        success: function (response) {
            if (response['result'] == 'failure') {
                alert('잘못된 로그인 정보')
            }
            if (response['result'] == 'success') {
                console.log('로그인 성공')
                let token = response['access_token']
                console.log(token);
                document.cookie = "Authorization" + "=" + token
            }
            else {
                alert('뭐지?')
            }
        }
    })
}

function signup(){
    $.ajax({
        type: "GET",
        url: "/signup",
        success: function (response){
            console.log("가자")
        }
    })
}