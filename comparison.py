import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def load_and_merge_data():
    biodiversity_df = pd.read_csv("final_biodiversity_dataset.csv")
    deforestation_df = pd.read_csv("cleaned_deforestation_dataset.csv")
    
    merged_df = pd.merge(
        biodiversity_df,
        deforestation_df,
        left_on="COU",
        right_on="Country_Code",
        how="inner"
    )
    
    if "Country_y" in merged_df.columns:
        merged_df.drop(columns=["Country_y"], inplace=True)
    if "Country_x" in merged_df.columns:
        merged_df.rename(columns={"Country_x": "Country"}, inplace=True)
    
    return merged_df

def biodiversity_efficiency(merged_df):
    merged_df["Biodiversity_Efficiency"] = merged_df["Animals"] / merged_df["Forest_Area_2020"]
    merged_df = merged_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Biodiversity_Efficiency"])
    
    efficient_countries = merged_df.nlargest(15, "Biodiversity_Efficiency")
    
    fig = px.bar(
        efficient_countries,
        x="Biodiversity_Efficiency",
        y="Country_Code",
        title="Top 15 Countries by Biodiversity Efficiency",
        color="Forest_Area_2020",
        orientation="h",
        color_continuous_scale="Viridis",
        labels={
            "Biodiversity_Efficiency": "Species per Forest Area %",
            "Country_Code": "Country",
            "Forest_Area_2020": "Forest Area (%)"
        }
    )
    return fig

def species_impact_analysis(merged_df):
    merged_df["Deforestation_Severity"] = pd.cut(
        merged_df["Forest_Change_Percentage"],
        bins=[-100, -20, -5, 0, 100],
        labels=["Severe", "Moderate", "Low", "Gain"]
    )
    
    severe_countries = merged_df[merged_df["Deforestation_Severity"] == "Severe"]["COU"].unique()
    species_impact = merged_df[merged_df["COU"].isin(severe_countries)].groupby("Species")["Animals"].sum().reset_index()
    species_impact = species_impact.sort_values("Animals", ascending=False)
    
    fig = px.bar(
        species_impact,
        x="Species",
        y="Animals",
        title="Species Most Affected in Countries with Severe Deforestation",
        color="Animals",
        color_continuous_scale="Reds",
        labels={"Animals": "Number of Species", "Species": "Species Type"}
    )
    return fig

def show():
    st.title("🌲 Deforestation vs. Endangered Species Analysis")
    
    merged_df = load_and_merge_data()
    
    st.sidebar.header("🔍 Filter Options")
    selected_country = st.sidebar.selectbox("🌍 Select Country", ['All'] + list(merged_df["Country"].unique()))
    selected_species = st.sidebar.selectbox("🐾 Select Species", ['All'] + list(merged_df["Species"].unique()))
    
    filtered_df = merged_df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df["Country"] == selected_country]
    if selected_species != 'All':
        filtered_df = filtered_df[filtered_df["Species"] == selected_species]
    
    st.subheader("📊 Filtered Dataset")
    st.dataframe(filtered_df)
    
    st.subheader("📊 Species Status by Country")
    species_status_df = filtered_df.groupby(["Country", "Status"])["Animals"].sum().reset_index()
    bar_fig = px.bar(
        species_status_df,
        x="Country",
        y="Animals",
        color="Status",
        title="Comparison of Endangered, Vulnerable, and Critical Species",
        labels={"Animals": "Number of Species"},
        barmode="stack"
    )
    st.plotly_chart(bar_fig)
    
    st.subheader("🥧 Species Distribution in Affected Countries")
    pie_df = filtered_df.groupby("Species")["Animals"].sum().reset_index()
    pie_fig = px.pie(
        pie_df,
        names="Species",
        values="Animals",
        title="Proportion of Different Species Affected by Deforestation",
        hole=0.4
    )
    st.plotly_chart(pie_fig)
    
    st.subheader("📊 Deforestation vs. Number of Endangered Species")
    scatter_fig = px.scatter(
        merged_df,
        x="Forest_Change_Percentage",
        y="Animals",
        color="Status",
        title="Forest Loss vs. Number of Endangered Species",
        labels={"Forest_Change_Percentage": "Forest Change (%)", "Animals": "Number of Species"},
        hover_data=["Country"]
    )
    st.plotly_chart(scatter_fig)
    
    st.subheader("📊 Biodiversity Efficiency")
    st.plotly_chart(biodiversity_efficiency(merged_df))
    
    st.write("📌 **Data Sources:**")
    st.write("🔗 [Biodiversity Dataset](https://www.kaggle.com/datasets/sarthakvajpayee/global-species-extinction)")
    st.write("🔗 [Deforestation Dataset](https://www.kaggle.com/datasets/konradb/deforestation-dataset/data)")

