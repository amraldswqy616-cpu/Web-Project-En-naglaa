
// 1. استنى لما الصفحة تجهز
document.addEventListener('DOMContentLoaded', function() {
    
    // 2. امسك فورم اللوجن وزرار الخطأ
    const loginForm = document.querySelector('form');
    const errorSpan = document.getElementById('login_password-err');

    // 3. لما المستخدم يدوس Login
    loginForm.onsubmit = function(event) {
        // امنع الصفحة إنها تحمل من جديد
        event.preventDefault();

        // امسح أي رسالة خطأ قديمة
        errorSpan.innerText = '';

        // 4. جمع البيانات (Username & Password)
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData);

        // 5. ابعت البيانات للسيرفر
        fetch('/check_login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(function(response) {
            return response.json(); // حول الرد لـ JSON
        })
        .then(function(result) {
            // لو البيانات صح
            if (result.status === "success") {
                window.location.href = result.redirect_url; // ادخل للموقع
            } 
            // لو فيه غلط في اليوزر أو الباسورد
            else {
                errorSpan.innerText = result.message; // اظهر الرسالة تحت المربع
            }
        })
        .catch(function(error) {
            console.log("Error:", error);
            alert("Connection error!");
        });
    };
});

