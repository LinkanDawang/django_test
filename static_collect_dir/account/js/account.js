// // 注册按钮提交
// $('#resub').click(function (event) {
//     var username = document.getElementById("re_name").value;
//     var email = document.getElementById("re_email").value;
//     var password = document.getElementById("re_pwd").value;
//
//     $.ajax({
//         async: false,
//         // url: "http://leslie.eacho.online/api/users/register/",
//         url: "http://127.0.0.1:8000/api/users/register/",
//         data: {"username": username, "email": email, "password": password},
//         type: "POST",
//         dataType: "json",
//         success: function(data){
//             console.log(data.msg)
//         }
//     })
// })