
import streamlit as st
import pandas as pd
import numpy as np
import joblib

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

st.set_page_config(page_title="Iris Prediction", layout="wide")

st.title("🌸 Iris Flower Prediction")

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target

classes = iris.target_names

# Train and save models
@st.cache_resource
def train_models():
    rf = RandomForestClassifier(random_state=42)
    lr = LogisticRegression(max_iter=200)

    # Compare model accuracy using cross-validation
    rf_accuracy = cross_val_score(rf, X, y, cv=5).mean()
    lr_accuracy = cross_val_score(lr, X, y, cv=5).mean()

    rf.fit(X, y)
    lr.fit(X, y)

    joblib.dump(rf, "model.pkl")
    joblib.dump(lr, "logistic_model.pkl")

    # Load saved models
    rf = joblib.load("model.pkl")
    lr = joblib.load("logistic_model.pkl")

    return rf, lr, rf_accuracy, lr_accuracy


rf, lr, rf_accuracy, lr_accuracy = train_models()

# Choose model
model_name = st.selectbox(
    "Choose Model",
    ["Random Forest", "Logistic Regression"]
)

model = rf if model_name == "Random Forest" else lr

# Input measurements
st.subheader("Enter Flower Measurements")

with st.form("flower_form"):
    sl = st.slider("Sepal Length", 4.0, 8.0, 5.1)
    sw = st.slider("Sepal Width", 2.0, 4.5, 3.5)
    pl = st.slider("Petal Length", 1.0, 7.0, 1.4)
    pw = st.slider("Petal Width", 0.1, 2.5, 0.2)

    submit = st.form_submit_button("Predict")

# Create prediction history
if "history" not in st.session_state:
    st.session_state.history = []

# Predict flower
if submit:
    data = np.array([[sl, sw, pl, pw]])

    prediction = model.predict(data)[0]
    probabilities = model.predict_proba(data)[0]

    flower = classes[prediction]

    st.success(f"Predicted Flower: {flower}")

    st.metric(
        "Confidence",
        f"{probabilities[prediction] * 100:.1f}%"
    )

    # Probability chart
    st.subheader("Class Probabilities")

    chart_data = pd.DataFrame({
        "Probability": probabilities
    }, index=classes)

    st.bar_chart(chart_data)

    # Save history
    st.session_state.history.append({
        "Model": model_name,
        "Prediction": flower,
        "Sepal Length": sl,
        "Sepal Width": sw,
        "Petal Length": pl,
        "Petal Width": pw
    })

# Show prediction history
st.subheader("Prediction History")

if st.session_state.history:
    history = pd.DataFrame(st.session_state.history)
    st.dataframe(history, use_container_width=True)
else:
    st.write("No predictions yet.")

# Compare models
st.subheader("Model Comparison")

comparison = pd.DataFrame({
    "Model": ["Random Forest", "Logistic Regression"],
    "Accuracy (%)": [
        round(rf_accuracy * 100, 2),
        round(lr_accuracy * 100, 2)
    ]
})

st.dataframe(comparison, use_container_width=True)
st.bar_chart(comparison.set_index("Model"))
