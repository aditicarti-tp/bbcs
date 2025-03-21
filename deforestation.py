import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry  # To map country codes to names automatically

def show():
    st.title("🌲 Deforestation Data Analysis")
    
    # Load cleaned dataset
    file_path = "cleaned_deforestation_dataset.csv"
    df = pd.read_csv(file_path)

    # Function to map country codes to country names
    def get_country_name(code):
        try:
            return pycountry.countries.get(alpha_3=code).name
        except:
            return code  # Return original code if not found

    # Add full country names
    df["Country_Name"] = df["Country_Code"].apply(get_country_name)

    # Sidebar Filter
    st.sidebar.header("🔍 Filter Options")
    selected_country = st.sidebar.selectbox("🌍 Select Country", ['All'] + list(df["Country_Name"].unique()))

    # Apply Filter
    filtered_df = df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df["Country_Name"] == selected_country]

    # 📄 Display full dataset
    st.subheader("📄 Complete Deforestation Dataset")
    st.dataframe(filtered_df)

    # 📊 1. Top 10 Countries with Most Forest Loss
    st.subheader("🔥 Top 10 Countries with the Highest Forest Loss")
    top_countries = df.nlargest(10, "Forest_Change_Percentage")

    fig_top_loss = px.bar(
        top_countries, x="Forest_Change_Percentage", y="Country_Name",
        title="Top 10 Countries with the Most Forest Loss",
        labels={"Forest_Change_Percentage": "Forest Loss (%)"},
        color="Forest_Change_Percentage",
        orientation="h",
        color_continuous_scale="oranges"
    )
    st.plotly_chart(fig_top_loss)
    st.write("🔍 **Insight:** These countries experienced the highest forest loss, likely due to deforestation, logging, and land conversion.")

    # 📉 2. Forest Area Change Over Time (Line Chart)
    st.subheader("📈 Forest Area Change Over Time")
    fig_line = px.line(
        df, x="Country_Name", y=["Forest_Area_2000", "Forest_Area_2020"],
        title="Forest Cover Change from 2000 to 2020",
        labels={"value": "Forest Area (%)"},
        markers=True
    )
    st.plotly_chart(fig_line)
    st.write("🔍 **Insight:** Comparing forest area in 2000 and 2020 highlights which countries lost the most forest cover.")

    # 🔥 3. Heatmap of Forest Loss
    st.subheader("🗺️ Global Forest Loss Heatmap")
    fig_map = px.choropleth(
        df, locations="Country_Code", locationmode="ISO-3",
        color="Forest_Change_Percentage",
        title="Global Deforestation Trends (2000-2020)",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig_map)
    st.write("🔍 **Insight:** Darker red regions show where deforestation is most severe.")

    st.write("📌 **Data Sources:**")
    st.write("🔗 [Biodiversity Dataset](https://www.kaggle.com/datasets/sarthakvajpayee/global-species-extinction)")
    st.write("🔗 [Deforestation Dataset](https://www.kaggle.com/datasets/konradb/deforestation-dataset/data)")

