import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("Deforestation vs. Endangered Species Analysis")

    # Load both datasets
    biodiversity_df = pd.read_csv("cleaned_biodiversity_dataset.csv")
    deforestation_df = pd.read_csv("cleaned_deforestation_dataset.csv")

    # Merge datasets on country code
    merged_df = pd.merge(
        biodiversity_df, 
        deforestation_df, 
        left_on="COU",  # Match biodiversity dataset
        right_on="Country_Code",  # Match deforestation dataset
        how="inner"
    )

    # Display merged dataset
    st.subheader("Merged Dataset (Biodiversity & Deforestation)")
    st.dataframe(merged_df)

    # Scatter Plot: Deforestation vs. Endangered Species
    st.subheader("Deforestation vs. Number of Endangered Species")
    scatter_fig = px.scatter(
        merged_df,
        x="Forest_Change_Percentage",
        y="Value",
        color="International Union for Conservation of Nature Category",
        title="Forest Loss vs. Number of Endangered Species",
        labels={"Forest_Change_Percentage": "Forest Change (%)", "Value": "Number of Species"},
        hover_data=["Country"]
    )
    st.plotly_chart(scatter_fig)

    # Bar Chart: Average Forest Loss and Species Count per Country
    st.subheader("Average Forest Loss and Species Count per Country")
    avg_data = merged_df.groupby("Country").agg(
        {"Forest_Change_Percentage": "mean", "Value": "sum"}
    ).reset_index()

    bar_fig = px.bar(
        avg_data,
        x="Country",
        y=["Forest_Change_Percentage", "Value"],
        title="Forest Loss and Endangered Species Count by Country",
        labels={"value": "Value", "variable": "Metric"},
        barmode="group"
    )
    st.plotly_chart(bar_fig)

    st.write("Data Source: Merged Biodiversity and Deforestation Dataset")
