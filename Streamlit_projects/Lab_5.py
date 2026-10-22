
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Page title
st.title("Data Visualization")

# Sample student marks
np.random.seed(42)

df = pd.DataFrame(
    np.random.randint(35, 101, size=(20, 3)),
    columns=["Math", "Science", "English"]
)

st.subheader("Sample Data")
st.dataframe(df)

# 1. Built-in charts
st.subheader("Built-in Charts")

st.write("Line Chart")
st.line_chart(df)

st.write("Bar Chart")
st.bar_chart(df)

st.write("Area Chart")
st.area_chart(df)

# 2. Matplotlib histogram
st.subheader("Matplotlib Chart")

fig, ax = plt.subplots()
ax.hist(df["Math"], bins=10, color="skyblue", edgecolor="black")
ax.set_title("Math Score Distribution")
ax.set_xlabel("Math Marks")
ax.set_ylabel("Number of Students")

st.pyplot(fig)
plt.close(fig)

# 3. Plotly histogram
st.subheader("Plotly Histogram")

fig_plotly = px.histogram(
    df,
    x="Math",
    nbins=10,
    title="Math Distribution"
)

st.plotly_chart(fig_plotly, use_container_width=True)

# 4. Scatter plot
st.subheader("Math vs Science")

st.scatter_chart(
    df,
    x="Math",
    y="Science"
)

# 5. Average score metric
st.subheader("Average Math Score")

average = df["Math"].mean()

st.metric(
    label="Average Math Score",
    value=f"{average:.2f}"
)
