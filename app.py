import streamlit as st
import biodiversity as biodiversity
import deforestation as deforestation
import comparison as comparison

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Biodiversity", "Deforestation", "Comparison"])

# Load the correct page
if page == "Biodiversity":
    biodiversity.show()
elif page == "Deforestation":
    deforestation.show()
elif page == "Comparison":
    comparison.show()
