
import streamlit as st

st.title("Layouts Demo")

# --- Sidebar ---
st.sidebar.header("Settings")

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Dark"]
)

font_size = st.sidebar.slider(
    "Font Size",
    10, 30, 15
)

# --- Columns ---
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", "25 Lakh")

with col2:
    st.metric("Customers", "1,200")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(
    ["Overview", "Analysis", "About"]
)

with tab1:
    st.write("Overview content here")

with tab2:
    st.write("Analysis content here")

with tab3:
    st.write("About this app")

# --- Container ---
with st.container():
    st.subheader("Grouped Section")
    st.write("All these elements are inside one container.")

# --- Display selected settings ---
st.write("Selected Theme:", theme)
st.write("Selected Font Size:", font_size)
