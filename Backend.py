from flask import Flask, request, redirect, render_template, url_for,jsonify
import pyodbc 

app = Flask(__name__)

# إعدادات الاتصال بقاعدة البيانات (تأكد من اسم السيرفر عندك)
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'  # تجده عند فتح SSMS
        'DATABASE=SoccerKicksDB;'
        'Trusted_Connection=yes;'
    )
    return conn


# 1. الصفحة الرئيسية (التي تظهر أول ما تفتح الموقع)
@app.route('/')
def index():
    return render_template('login.html') # تأكد أن الملف موجود داخل مجلد اسمه templates


# 2. استقبال بيانات الدخول
@app.route('/check_login', methods=['POST'])
def check_login():
    # استلام البيانات كـ JSON
    data = request.get_json()
    user_input = data.get('username', '').strip()
    pass_input = data.get('password', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
    cursor.execute(query, (user_input, pass_input))
    user = cursor.fetchone()
    conn.close()

    if user:
        # لو نجح، بنبعت نجاح ورابط الصفحة اللي هيروح لها (مثلاً الـ Home)
        return jsonify({
            "status": "success", 
            "redirect_url": url_for('home_page')
        })
    else:
        # لو فشل، بنبعت رسالة الخطأ ونحدد الـ field اللي هتظهر تحته
        # هنا ممكن نثبتها تحت حقل الباسورد مثلاً
        return jsonify({
            "status": "error", 
            "field": "login_password", 
            "message": "Invalid username or password!"
        }), 401

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    data=request.get_json()
    f_name = data.get('first_name')
    l_name = data.get('last_name')
    email = data.get('email') 
    uname = data.get('username')
    pword = data.get('password')
    pword_confirm = data.get('reset_password')

    # --- مرحلة التحقق الهندسية (Validation) ---

    # 1. التحقق من تطابق كلمة المرور
    if pword != pword_confirm:
        return jsonify({"status": "error", "field": "reset_password", "message": "Passwords do not match!"}), 400

    # 2. التحقق من طول كلمة المرور (8 حروف على الأقل)
    if len(pword) < 8:
        return jsonify({"status": "error", "field": "password", "message": "Password At least 8 characters required!"}), 400

    # 3. التحقق أن اسم المستخدم يبدأ بحرف وليس رقم
    if not f_name[0].isalpha():
        return jsonify({"status": "error", "field": "first_name", "message": "First name Must start with a letter!"}), 400    
    if not l_name[0].isalpha():
        return jsonify({"status": "error", "field": "last_name", "message": " last name Must start with a letter!"}), 400
    if not email[0].isalpha():
        return jsonify({"status": "error", "field": "email", "message": "Email Must start with a letter!"}), 400   
    
    if not uname[0].isalpha():
        return jsonify({"status": "error", "field": "username", "message": " User name Must start with a letter!"}), 400

    # --- مرحلة قاعدة البيانات ---
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # التأكد من أن اسم المستخدم غير موجود مسبقاً
        cursor.execute("SELECT Username FROM Users WHERE Username = ?", (uname,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": "error", "field": "Username_Exsiting", "message": "Username already Exist"}), 400

        # تنفيذ عملية الإضافة
        query = """
            INSERT INTO Users (Username, Password, FirstName, LastName, Email)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (uname, pword, f_name, l_name, email))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Account created! Redirecting..."}), 200    
    except Exception as e:
       return redirect(url_for('signup_page', error='Database error occurred!'))

# تأكد أن اسم الدالة هنا هو login كما اكتشفنا في الـ BuildError


# 3. مسار الصفحة الرئيسية (مستقل تماماً)
@app.route('/home')
def home_page():
    return render_template('index.html') # هنا نعرض صفحة المنتجات

if __name__ == '__main__':
    # تشغيل السيرفر ليكون متاحاً لك وللموبايل
    app.run(debug=True, host='0.0.0.0', port=5000)