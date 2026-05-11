// function valdition (){
// let username=document.getElementById("username").value
// let password=document.getElementById("password").value
// console.log("Hello "+username)
// }

const loginForm = document.getElementById("loginForm");
const passError = document.getElementById("passError");

loginForm.onsubmit = function(event) {
    let password = document.getElementById("password").value;
    let username = document.getElementById("username").value;

    // الشرط: التأكد أن الباسوورد لا يقل عن 8 أرقام/حروف
    if (password.length < 8 ) {
        // 1. منع إرسال الفورم للباك إند
        event.preventDefault(); 
        
        // 2. تنبيه المستخدم وتغيير النص ولونه
        passError.textContent = "⚠️ Password must be at least 8 characters!";
        document.getElementById("password").style.border = "2px solid red";
        
        console.log("Validation failed: Password too short.");
    } 
};