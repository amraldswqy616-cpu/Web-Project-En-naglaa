// استنى لما الصفحة تحمل بالكامل
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. امسك الفورم من الـ HTML
    const signupForm = document.querySelector('form');

    // 2. لما المستخدم يدوس على زرار الإرسال (Submit)
    signupForm.onsubmit = function(event) {
        // امنع الصفحة إنها تعمل Refresh
        event.preventDefault();

        // امسح أي رسائل خطأ قديمة كانت مكتوبة
        document.querySelectorAll('.error-msg').forEach(function(el) {
            el.innerText = '';
        });

        // 3. جمع البيانات من الفورم وجهزها في شكل JSON
        const formData = new FormData(signupForm);
        const data = Object.fromEntries(formData);

        // 4. ابعت الطلب للسيرفر (Fetch)
        fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(function(response) {
            // حول رد السيرفر لنص نقدر نقراه (JSON)
            return response.json();
        })
        .then(function(result) {
            // لو السيرفر قال "تم بنجاح"
            if (result.status === "success") {
                alert(result.message);
                window.location.href = '/'; // روح لصفحة اللوجن
            } 
            // لو السيرفر قال فيه "خطأ"
            else {
                // دور على الـ span اللي واخد الـ id بتاع الغلط واكتب فيه الرسالة
                const errorSpan = document.getElementById(result.field + '-err');
                if (errorSpan) {
                    errorSpan.innerText = result.message;
                }
            }
        })
        .catch(function(error) {
            // لو حصلت مشكلة في النت أو السيرفر وقع
            console.log("Error logic: ", error);
            alert("Connection error!");
        });
    };
});