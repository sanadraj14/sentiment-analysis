# 🛍 Sentiment Analysis Web App (Myntra Product Reviews)

A Flask-based web application that performs **sentiment analysis** on Myntra product reviews using a trained machine learning model.  
It features **user authentication (login/register)**, a **prediction dashboard**, and a **history page** with **animated charts** (pie/bar) to visualize sentiment distribution.  
The UI is styled with **Bootstrap 5** and **Animate.css** for a modern, animated experience.

---

## 🚀 Features
- 🔑 **User Authentication**: Register, login, and logout with secure password hashing.
- 📝 **Sentiment Prediction**: Enter product reviews and get instant sentiment classification (Positive / Negative / Neutral).
- 📜 **Prediction History**: View all past predictions stored in a MySQL database.
- 📊 **Charts**: Pie and bar charts show sentiment distribution dynamically.
- 🎨 **Animated UI**: Sidebar navigation, animated forms, and result cards.

---

## 📂 Project Structure
sentiment-analysis-app/
│
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── model.pkl             # Trained ML model
├── vectorizer.pkl        # Saved vectorizer
├── templates/            # HTML templates
│   ├── base.html         # Shared layout (sidebar, styles)
│   ├── home.html         # Dashboard home
│   ├── index.html        # Prediction page
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   └── history.html      # History + charts
└── static/               # Optional CSS/JS/images

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/sentiment-analysis-app.git
cd sentiment-analysis-app

2. Install Dependencies
pip install -r requirements.txt

3. Run the app
python app.py

📊 Example Usage
- Register a new account.
- Login with your credentials.
- Navigate to Predict and enter a Myntra product review:

"The kurta quality is amazing and delivery was super fast!"

- Get instant sentiment classification with confidence score.
- Check History to see all past predictions and view sentiment distribution charts.

✨  Future Improvements
- Support batch analysis of multiple reviews.
- Deploy on cloud (Heroku/AWS/Render).
- Add more interactive charts (line chart for trends over time).
 
 👨‍💻 Author
Developed during August Internship 2025 by Sahana D Raj.

📌 Place this file as `README.md` in your project’s **root folder** (same level as `app.py` and `requirements.txt`). GitHub will automatically display it when someone visits your repository.  



