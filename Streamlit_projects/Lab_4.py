import streamlit as st

st.title("Forms + Session State")

# --- Initialize Session State ---
if "count" not in st.session_state:
    st.session_state.count = 0

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "todos" not in st.session_state:
    st.session_state.todos = []

# --- Counter ---
st.subheader("Counter")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Increment"):
        st.session_state.count += 1

with col2:
    if st.button("Add 5"):
        st.session_state.count += 5

with col3:
    if st.button("Reset Counter"):
        st.session_state.count = 0

st.metric("Current Counter", st.session_state.count)

# --- Login Form ---
st.subheader("Login Form")

with st.form("login_form"):
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if user == "admin" and pwd == "1234":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.session_state.logged_in = False
        st.error("Invalid credentials!")

if st.session_state.logged_in:
    st.info("Welcome, admin! You are now logged in.")

# --- To-Do List Form ---
st.subheader("To-Do List")

with st.form("todo_form", clear_on_submit=True):
    task = st.text_input("Enter a new task")
    add = st.form_submit_button("Add Task")

if add:
    if task.strip():
        st.session_state.todos.append(task.strip())
        st.success("Task added successfully!")
    else:
        st.warning("Please enter a task.")

# Display tasks
st.subheader("Your Tasks")

if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos, start=1):
        st.write(f"{i}. {todo}")
else:
    st.write("No tasks added yet.")

# Clear all tasks
if st.button("Clear All Tasks"):
    st.session_state.todos = []
    st.success("All tasks cleared!")
