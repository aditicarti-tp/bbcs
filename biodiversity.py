import streamlit as st
import pandas as pd
import plotly.express as px

def show(): 
    # Load dataset
    file_path = "cleaned_bird_datafinall.csv"
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

    # Top 10 Countries with Most Endangered Species (Including "CRIT")
    st.subheader("🌍 Top 10 Countries with Most Endangered Species")
    endangered_df = df[df["Status"].isin(["THREAT", "VULN", "CRIT"])]  # Filter for threatened, vulnerable, and critical species
    top_countries = endangered_df.groupby("Country")["Animals"].sum().nlargest(10).reset_index()

    fig_top_countries = px.bar(
        top_countries, x="Animals", y="Country",
        title="Top 10 Countries with Most Endangered Species",
        labels={"Animals": "Number of Endangered Species"},
        color="Animals",
        orientation="h",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig_top_countries)
    st.write("🔍 **Insight:** These countries have the highest number of endangered species. They may need urgent conservation efforts.")

    # Species Distribution Over Countries (Bubble Chart)
    st.subheader("Endangered, Vulnerable, Critical, and Known Species Distribution")
    fig_bubble = px.scatter(
        df[df["Status"].isin(["THREAT", "VULN", "CRIT"])],  # Include "CRIT" for Critical species
        x="Country", y="Animals", size="Animals",
        color="Status",
        title="Distribution of At-Risk Species by Country",
        labels={"Animals": "Number of Species"},
        color_discrete_map={
            "THREAT": "red", 
            "VULN": "orange", 
            "CRIT": "blue",  # Added color for Critical status
            "KNOW": "green"
        }
    )
    st.plotly_chart(fig_bubble)
    st.write("🔍 **Insight:** Larger bubbles indicate a greater number of species at risk in that country.")

    # Comparison of Endangered, Vulnerable, Critical, and Known Species by Country
    st.subheader("Conservation Status Comparison")

    # Define categories and colors
    conservation_categories = ["THREAT", "VULN", "CRIT", "KNOW"]
    colors = {"THREAT": "#d62728", "VULN": "#ff7f0e", "CRIT": "#1f77b4", "KNOW": "#2ca02c"}

    for category in conservation_categories:
        category_df = df[df["Status"] == category]
        if not category_df.empty:
            st.subheader(f"{category} Species by Country")
            fig = px.bar(
                category_df, x="Country", y="Animals", 
                labels={"Animals": "Number of Species"},
                title=f"{category} Species Distribution",
                color_discrete_sequence=[colors[category]]
            )
            st.plotly_chart(fig)

    st.write("🔍 **Insight:** This breakdown allows us to compare different levels of species risk across various countries.")

    st.write("📌 **Data Source:** Biodiversity Dataset")
