// 날씨 검색
function login() {

    $.ajax({
      type: "POST",
      url: "/user/login",
      data: { 
        'email' : $("#userEmail").val(),
        'pwd' : $("#userPassword").val(),
      },
      success: function (data) {
        location.href = '/weather'
      },
      error: function (xhr) {

        if(xhr.status == 401) {
            alert("가입되지 않은 이메일입니다.")
        }
        else if(xhr.status == 403) {
            alert("로그인 정보가 일치하지 않습니다.")
        }
      },
    });
  }
  