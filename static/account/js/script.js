const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const regButton = document.getElementById('resub');
const loginButton = document.getElementById('login');


signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});


signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});


// 用户注册
regButton.addEventListener("click", () => {
    const username = document.getElementById("re_name").value;
    const email = document.getElementById("re_email").value;
    const password = document.getElementById("re_pwd").value;

    // 邮箱校验
    // var mailreg = new RegExp('^([a-zA-Z0-9]+[_|\\_|\\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\\_|\\.]?)*[a-zA-Z0-9]+\\.[a-zA-Z]{2,3}$', '');
    // var isPass = mailreg.test(email)
    // if (isPass == false){
    //     alert("邮箱格式错误")
    // }
    // else {
    // }

    $.ajax({
        // url: "http://leslie.eacho.online/api/users/register/",
        url: "http://127.0.0.1:8000/api/users/register/",
        data: {"username": username, "email": email, "password": password},
        type: "post",
        dataType: "json",
        // headers: {"Access-Control-Allow-Origin": "*"},
        success: function(data){
            if (data.code==200){
                alert("注册成功，请到邮箱激活账号");
                window.location='';  // todo 跳转到其他页面
            }
            else {
                alert(data.msg);
            }
        }
    })
});

// 用户登入
loginButton.addEventListener("click", () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    $.ajax({
        url: "http://127.0.0.1:8000/api/users/login/",
        data: {"username": username, "password": password},
        type: "POST",
        dataType: "json",
        success: function (data) {
            if (data.code == 200){
                alert("登入成功");
                window.open("index/index.html");
            }
            else {
                alert(data.msg);
            }
        }
    })
});
