// 로그인
function login() {

  var email = $("#userEmail").val();
  var pwd = $("#userPassword").val();

    $.ajax({
      type: "POST",
      url: "/user/login",
      data: { 
        'email' : email,
        'pwd' : pwd
      },
      success: function (data) {
        location.href = '/weather';
      },
      error: function (xhr) {

        if(xhr.status == 401) {
            alert("가입되지 않은 이메일입니다.");
        }
        else if(xhr.status == 403) {
            alert("로그인 정보가 일치하지 않습니다.");
        }
      },
    });
  }


// 회원가입
function signupView() {
  location.href = "/user/signupview";
}

  