import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("🌲 Deforestation vs. Endangered Species Analysis")

    # Load both datasets
    biodiversity_df = pd.read_csv("cleaned_biodiversity_dataset.csv")
    deforestation_df = pd.read_csv("cleaned_deforestation_dataset.csv")

    # Merge datasets on country code
    merged_df = pd.merge(
        biodiversity_df, 
        deforestation_df, 
        left_on="COU",  
        right_on="Country_Code",  
        how="inner"
    )

    # Drop duplicate country column if it exists
    if "Country_y" in merged_df.columns:
        merged_df.drop(columns=["Country_y"], inplace=True)
    if "Country_x" in merged_df.columns:
        merged_df.rename(columns={"Country_x": "Country"}, inplace=True)

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Options")
    selected_country = st.sidebar.selectbox("🌍 Select Country", ['All'] + list(merged_df["Country"].unique()))
    selected_species = st.sidebar.selectbox("🐾 Select Species", ['All'] + list(merged_df["Species"].unique()))

    # Apply Filters
    filtered_df = merged_df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df["Country"] == selected_country]
    if selected_species != 'All':
        filtered_df = filtered_df[filtered_df["Species"] == selected_species]

    # Display filtered dataset
    st.subheader("📊 Filtered Comparison Dataset")
    st.dataframe(filtered_df)

    # 📊 Stacked Bar Chart: Endangered vs. Vulnerable vs. Critical Species
    st.subheader("📊 Species Status by Country")

    species_status_df = filtered_df.groupby(["Country", "International Union for Conservation of Nature Category"])["Value"].sum().reset_index()

    bar_fig = px.bar(
        species_status_df,
        x="Country",
        y="Value",
        color="International Union for Conservation of Nature Category",
        title="Comparison of Endangered, Vulnerable, and Critical Species",
        labels={"Value": "Number of Species"},
        barmode="stack"
    )
    st.plotly_chart(bar_fig)
    st.write("🔍 **Insight:** This shows the biodiversity loss breakdown in each country.")

    # 🥧 Pie Chart: Species Distribution in Deforestation-Affected Areas
    st.subheader("🥧 Species Distribution in Affected Countries")

    pie_df = filtered_df.groupby("Species")["Value"].sum().reset_index()

    pie_fig = px.pie(
        pie_df,
        names="Species",
        values="Value",
        title="Proportion of Different Species Affected by Deforestation",
        hole=0.4
    )
    st.plotly_chart(pie_fig)
    st.write("🔍 **Insight:** This pie chart shows which species are most affected by deforestation.")

    st.write("📌 **Data Source:** Merged Biodiversity & Deforestation Dataset")
