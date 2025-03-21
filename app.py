import streamlit as st
import pages.biodiversity as biodiversity
import pages.deforestation as deforestation
import pages.comparison as comparison

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
