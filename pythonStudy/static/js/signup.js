


// 회원가입 화면
function signupview() {}

// 회원가입
function signup() {

  email = $('#email').val();
  username = $('#username').val();
  password = $('#password').val();

  $.ajax({
    type: "POST",
    url: "/user/signup",
    data: {
      'email': email,
      'name': username,
      'password': password,
    },
    success : function() {
      location.href = '/user/loginview'
      alert("회원가입 성공!")
    }
  });
}


