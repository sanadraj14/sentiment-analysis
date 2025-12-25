from flask import Flask, request, render_template, redirect, url_for, session, flash
import pickle
import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# ---------------------------
# Flask app
# ---------------------------
app = Flask(__name__)
app.secret_key = "replace_this_with_a_secure_random_key"

# ---------------------------
# Load ML model and vectorizer
# ---------------------------
MODEL_PATH = r"C:\Users\Sahana D Raju\OneDrive\Desktop\August Internship\internship 2025\sentiment-analysis\model.pkl"
VEC_PATH = r"C:\Users\Sahana D Raju\OneDrive\Desktop\August Internship\internship 2025\sentiment-analysis\vectorizer.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VEC_PATH, "rb") as f:
    vectorizer = pickle.load(f)

# ---------------------------
# Database connection and initialization
# ---------------------------
def get_db_connection(create_db=False):
    try:
        if create_db:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",   # Add your MySQL password if required
                cursorclass=DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS sentiment_analysis")
            conn.close()
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",   # Add your MySQL password if required
            database="sentiment_analysis",
            cursorclass=DictCursor
        )
        return conn
    except pymysql.MySQLError as err:
        print("❌ Database connection error:", err)
        return None

def init_db():
    conn = get_db_connection(create_db=True)
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        input_text TEXT NOT NULL,
                        predicted_label VARCHAR(20) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()
            print("✅ Database tables initialized successfully!")
        except Exception as e:
            print("❌ Error initializing database:", e)
        finally:
            conn.close()

# ---------------------------
# Login required decorator
# ---------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("⚠ Please log in first!", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", username=session.get("username"))
    else:
        return render_template("home.html")  # or landing.html if you create one

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    if request.method == "GET":
        return render_template("index.html")

    input_text = request.form.get("text", "").strip()
    if not input_text:
        flash("⚠ Please enter some text!", "error")
        return render_template("index.html")

    # ML Prediction
    input_vec = vectorizer.transform([input_text])
    prediction = model.predict(input_vec)[0]

    # Store in DB
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO predictions (input_text, predicted_label) VALUES (%s, %s)",
                    (input_text, prediction)
                )
            conn.commit()
        except Exception as e:
            print("❌ Database insert error:", e)
        finally:
            conn.close()

    return render_template("index.html", input_text=input_text, prediction=prediction)

@app.route("/history")
@login_required
def history():
    rows = []
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, input_text, predicted_label, created_at "
                    "FROM predictions ORDER BY created_at DESC"
                )
                rows = cursor.fetchall()
                # Count sentiments
                for r in rows:
                    label = r["predicted_label"]
                    if label in sentiment_counts:
                        sentiment_counts[label] += 1
        except Exception as e:
            print("❌ Database error:", e)
        finally:
            conn.close()

    return render_template("history.html", predictions=rows, sentiment_counts=sentiment_counts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()
        user = None
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
                    user = cursor.fetchone()
            except Exception as e:
                print("❌ Database error:", e)
            finally:
                conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["username"] = user["username"]
            flash(f"👋 Welcome back, {user['username']}!", "success")
            return redirect(url_for("home"))
        else:
            flash("❌ Invalid username or password!", "error")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        if not username or not email or not password:
            flash("⚠ Please fill all fields!", "error")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
                    if cursor.fetchone():
                        flash("⚠ Username or email already exists!", "error")
                        return render_template("register.html")

                    cursor.execute(
                        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                        (username, email, hashed_password)
                    )
                conn.commit()
            except Exception as e:
                print("❌ Error in register:", e)
                flash("⚠ Something went wrong. Try again.", "error")
            finally:
                conn.close()

        flash("✅ Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("✅ You have been logged out.")
    return redirect(url_for("home"))

# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)