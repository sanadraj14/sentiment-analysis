import pandas
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Load dataset
df = pandas.read_csv("product_reviews.csv")
print(f"Loaded dataset with {len(df)} samples")
print(df.head())

# Check for missing values
if df.isnull().sum().sum() > 0:
    print("⚠ Warning: Missing values found. Dropping them.")
    df = df.dropna()
    print(f"After dropping, {len(df)} samples remain")

# 2. Features and labels
X = df["review"]
y = df["sentiment"].str.title()  # Capitalize first letter to match app.py expectations

# 3. Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train set: {len(X_train)} samples, Test set: {len(X_test)} samples")
print(f"Train labels: {y_train.value_counts().to_dict()}")
print(f"Test labels: {y_test.value_counts().to_dict()}")

# 4. Convert text to numbers
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. Train a simple model
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# 6. Evaluate
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model accuracy on test set: {accuracy:.2f}")
print(f"Predictions: {list(y_pred)}")
print(f"Actual: {list(y_test)}")

# 7. Save the model and vectorizer
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved!")