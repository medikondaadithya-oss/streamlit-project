
import streamlit as st

# Page configuration - must be the FIRST Streamlit command
st.set_page_config(
    page_title="Hello App",
    page_icon="S",
    layout="centered"
)

# Text elements
st.title("Hello Streamlit")
st.header("My First App")
st.subheader("Learning Basics")
st.write("Streamlit converts Python scripts into web apps.")

st.markdown("**Bold**, *Italic*, and `code` work here.")
st. divider ()
# Messages
st.success("App loaded successfully!")
st.info("This is an info message.")
st.warning("This is a warning.")
st.error("This is an error.")
st. divider ()

# Simple inputs
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=100)

# Display user details
st.write(f"Hello, {name}!")
st.write(f"Your age is {age}.")

# Display data as a table
st.subheader("Sample Data")

st.table({
    "Name": ["A", "B"],
    "Marks": [85, 90]
})
