function login(){
    let user_id = $("#user_id").val();
    let user_password = $("#user_password").val();
    $("body").empty
    // document.getElementById("user_id").value = null;
    // document.getElementById("user_password").value = null;
    console.log("포스트 시작")
    $("body").empty
    $.ajax({
        type: "POST",
        url: "/login",
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({"user_id" : user_id, "user_password" : user_password}),
        success: function (response) {
            console.log("뭔가 옴")
            let message = response['result']
            console.log(message)
            if (message == 'failure') {
                alert('잘못된 로그인 정보')
            }
            if (message == 'success') {
                let token = response['access_token']
                console.log('로그인 성공')
                document.cookie = "Authorization" + "=" + token
                window.location.reload()
            }
            else {
                alert('뭐지?')
            }
        }
    })

  

}


function logout() {
        document.cookie = "Authorization" + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        console.log("로그아웃 되셨습니다.")
    }