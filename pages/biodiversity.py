import streamlit as st
import pandas as pd
import plotly.express as px

def show(): 
    # Load dataset
    file_path = "cleaned_biodiversity_dataset.csv"
    df = pd.read_csv(file_path)

    # Streamlit UI
    st.title("🌱 Biodiversity Data Dashboard")
    st.sidebar.header("🔍 Filter Options")

    # Dropdown filters
    countries = df["Country"].unique()
    species = df["Species"].unique()

    selected_country = st.sidebar.selectbox("🌍 Select Country", ['All'] + list(countries))
    selected_species = st.sidebar.selectbox("🦉 Select Species", ['All'] + list(species))

    # Filter data based on selection
    filtered_df = df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df["Country"] == selected_country]
    if selected_species != 'All':
        filtered_df = filtered_df[filtered_df["Species"] == selected_species]

    # Display full dataset
    st.subheader("📄 Complete Dataset")
    st.dataframe(filtered_df)

    # Top 10 Countries with Most Endangered Species
    st.subheader("🌍 Top 10 Countries with Most Endangered Species")
    endangered_df = df[df["International Union for Conservation of Nature Category"] == "ENDANGERED"]
    top_countries = endangered_df.groupby("Country")["Value"].sum().nlargest(10).reset_index()

    fig_top_countries = px.bar(
        top_countries, x="Value", y="Country",
        title="Top 10 Countries with Most Endangered Species",
        labels={"Value": "Number of Endangered Species"},
        color="Value",
        orientation="h",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig_top_countries)
    st.write("🔍 **Insight:** These countries have the highest number of endangered species. They may need urgent conservation efforts.")

    # Species Distribution Over Countries (Bubble Chart)
    st.subheader("Endangered, Vulnerable, and Critical Species Distribution")
    fig_bubble = px.scatter(
        df[df["International Union for Conservation of Nature Category"].isin(["ENDANGERED", "VULNERABLE", "CRITICAL"])],
        x="Country", y="Value", size="Value",
        color="International Union for Conservation of Nature Category",
        title="Distribution of At-Risk Species by Country",
        labels={"Value": "Number of Species"},
        color_discrete_map={"ENDANGERED": "red", "VULNERABLE": "orange", "CRITICAL": "blue"}
    )
    st.plotly_chart(fig_bubble)
    st.write("🔍 **Insight:** Larger bubbles indicate a greater number of species at risk in that country.")

    # Comparison of Endangered, Vulnerable, and Critical Species by Country
    st.subheader("Conservation Status Comparison")

    # Define categories and colors
    conservation_categories = ["ENDANGERED", "VULNERABLE", "CRITICAL"]
    colors = {"ENDANGERED": "#d62728", "VULNERABLE": "#ff7f0e", "CRITICAL": "#1f77b4"}

    for category in conservation_categories:
        category_df = df[df["International Union for Conservation of Nature Category"] == category]
        if not category_df.empty:
            st.subheader(f"{category} Species by Country")
            fig = px.bar(
                category_df, x="Country", y="Value", 
                labels={"Value": "Number of Species"},
                title=f"{category} Species Distribution",
                color_discrete_sequence=[colors[category]]
            )
            st.plotly_chart(fig)

    st.write("🔍 **Insight:** This breakdown allows us to compare different levels of species risk across various countries.")

    st.write("📌 **Data Source:** Biodiversity Dataset")
