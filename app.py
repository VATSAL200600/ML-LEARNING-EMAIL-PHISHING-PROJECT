from flask import Flask, render_template, request
import joblib
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Load model & vectorizer
model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Same cleaning function used in training
def clean_email(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' ', text)
    text = re.sub(r'\W+', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stopwords.words('english')]
    return " ".join(words)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        email_text = request.form["email"]
        clean_text = clean_email(email_text)
        vector = vectorizer.transform([clean_text])
        result = model.predict(vector)[0]

        prediction = "🚨 Phishing Email" if result == 1 else "✅ Safe Email"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
