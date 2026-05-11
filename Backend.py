from flask import Flask, request, redirect, render_template, url_for
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
def login():
    user_input = request.form.get('username', '').strip()
    pass_input = request.form.get('password', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
    cursor.execute(query, (user_input, pass_input))
    user = cursor.fetchone()

    conn.close()

    if user:
        # لو نجح، "وجهه" لمسار الصفحة الرئيسية الجديد
        return redirect(url_for('home_page')) 
    else:
       return redirect(url_for('index', error='Invalid username or password!'))

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    f_name = request.form.get('first_name')
    l_name = request.form.get('last_name')
    email = request.form.get('email')
    uname = request.form.get('username')
    pword = request.form.get('password')
    pword_confirm = request.form.get('reset_password')

    # --- مرحلة التحقق الهندسية (Validation) ---

    # 1. التحقق من تطابق كلمة المرور
    if pword != pword_confirm:
        return redirect(url_for('signup_page', error='Passwords do not match!'))

    # 2. التحقق من طول كلمة المرور (8 حروف على الأقل)
    if len(pword) < 8:
        return redirect(url_for('signup_page', error='Password must be at least 8 characters!'))

    # 3. التحقق أن اسم المستخدم يبدأ بحرف وليس رقم
    if not f_name[0].isalpha():
        return redirect(url_for('signup_page', error='First name must start with a letter!'))
    
    if not l_name[0].isalpha():
        return redirect(url_for('signup_page', error='Last name  must start with a letter!'))
    
    if not uname[0].isalpha():
        return redirect(url_for('signup_page', error='Username must start with a letter!'))

    # --- مرحلة قاعدة البيانات ---
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # التأكد من أن اسم المستخدم غير موجود مسبقاً
        cursor.execute("SELECT Username FROM Users WHERE Username = ?", (uname,))
        if cursor.fetchone():
            conn.close()
            return redirect(url_for('signup_page', error='Username already exists!'))

        # تنفيذ عملية الإضافة
        query = """
            INSERT INTO Users (Username, Password, FirstName, LastName, Email)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (uname, pword, f_name, l_name, email))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index', success='Account created successfully!'))
    
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