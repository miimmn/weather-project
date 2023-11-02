
// 회원가입
function signup() {

  var email = $('#email').val();
  var username = $('#username').val();
  var password = $('#password').val();

  if( email.trim() == '' || username.trim() == '' || password.trim() == '') {
    alert("입력값을 모두 입력하세요.");
    return;
  }

  $.ajax({
    type: "POST",
    url: "/user/signup",
    data: {
      'email': email,
      'name': username,
      'password': password,
    },
    success : function() {
      location.href = '/user/loginview';
      alert("회원가입 성공!");
    },
    error : function(xhr) {     
      if(xhr.status == 400) {
        alert("이미 존재하는 이메일입니다.");
      }
    }
  });
}


