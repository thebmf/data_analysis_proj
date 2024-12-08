import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import plotly.express as px
import zipfile

# App title
st.title("🔎 Terrorism Activity Analysis")
st.sidebar.title("🌍 Navigation")
section = st.sidebar.selectbox(
    "📂 Choose a section:",
    [
        "About the Project",
        "Data Overview",
        "Exploratory Data Analysis (EDA)",
        "Trend Visualization",
        "Hypothesis: Weapon Choice and Casualties",
        "Conclusions",
    ],
)


# Load data
@st.cache_data
def load_data():
    path_to_dataset = "backend/globalterrorismdb_0718dist.zip"
    with zipfile.ZipFile(path_to_dataset, "r") as z:
        # List all the files in the ZIP archive
        file_names = z.namelist()

        # Assuming there's only one CSV file in the ZIP
        csv_file_name = [name for name in file_names if name.endswith(".csv")][0]

        # Open the CSV file directly
        with z.open(csv_file_name) as f:
            df = pd.read_csv(f, encoding="ISO-8859-1")
    # df = pd.read_csv(path_to_dataset, encoding="ISO-8859-1")
    df = df[
        [
            "iyear",
            "imonth",
            "country_txt",
            "region_txt",
            "latitude",
            "longitude",
            "success",
            "attacktype1_txt",
            "targtype1_txt",
            "natlty1_txt",
            "gname",
            "weaptype1_txt",
            "nkill",
            "nwound",
        ]
    ]
    df = df.rename(
        columns={
            "iyear": "Year",
            "imonth": "Month",
            "country_txt": "Country",
            "region_txt": "Region",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "success": "Success_Status",
            "attacktype1_txt": "Attack_Type",
            "targtype1_txt": "Target_Type",
            "natlty1_txt": "Nationality",
            "gname": "Group_Name",
            "weaptype1_txt": "Weapon_Type",
            "nkill": "Num_Killed",
            "nwound": "Num_Wounded",
        }
    )
    df["Total_Casualties"] = df["Num_Killed"].fillna(0) + df["Num_Wounded"].fillna(0)
    df["Weapon_Type"] = df["Weapon_Type"].fillna("Unknown")
    df["Weapon_Type"] = df["Weapon_Type"].apply(
        lambda x: "Vehicle" if x == "Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)" else x
    )
    return df


df = load_data()

# About the Project
if section == "About the Project":
    st.header("📌 About the Project")
    st.write(
        """
        This application analyzes global terrorism activity data.
        It explores trends, key patterns, and hypotheses related to weapon choices and casualty counts.
        """
    )
    st.markdown(
        """
        **Analysis Stages:**
        1. Data cleaning and preprocessing
        2. Exploratory Data Analysis (EDA)
        3. Visualizing key trends and patterns
        4. Hypothesis testing on weapon choices
        """
    )

# Data Overview
elif section == "Data Overview":
    st.header("📋 Data Overview")
    st.write(
        """
        This stage presents the main parameters of the loaded dataset, covering global terrorist events, 
        including countries, regions, weapons, and casualties.
        """
    )
    st.subheader("📂 Sample Data")
    st.dataframe(df.head(10))
    st.write(
        """
        **Key Statistics:** The following table provides an overview of the dataset, including minimum, 
        maximum, and average values.
        """
    )
    st.write(df.describe())
    st.subheader("🛠️ Missing Values")
    st.write(
        """
        Analyzing missing data helps assess the dataset quality and determine the need for further processing steps.
        """
    )
    st.write(df.isnull().sum())

# Exploratory Data Analysis (EDA)
elif section == "Exploratory Data Analysis (EDA)":
    st.header("📊 Exploratory Data Analysis (EDA)")
    st.subheader("📅 Number of Events Over the Years")
    st.write(
        """
        Analyzing the number of events by year highlights the dynamics of terrorist activity.
        This chart identifies peaks and changes over time.
        """
    )
    yearly_counts = df["Year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    yearly_counts.plot(kind="bar", color="darkgreen", ax=ax)
    ax.set_title("Number of Events by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Events")
    st.pyplot(fig)

    st.subheader("🌍 Top 10 Countries by Number of Events")
    st.write(
        """
        This section highlights the countries most frequently involved in terrorist incidents.
        """
    )
    top_countries = df["Country"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    top_countries.plot(kind="bar", color="darkblue", ax=ax)
    ax.set_title("Top 10 Countries by Number of Events")
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of Events")
    st.pyplot(fig)

    st.subheader("🌍 Distribution of Attack Types")
    st.write(
        """
        This section shows the types of attacks used in terrorist incidents.
        """
    )
    attack_types = df["Attack_Type"].value_counts()
    percentages = (attack_types / attack_types.sum() * 100).round(1)

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts = ax.pie(attack_types, startangle=90, colors=plt.cm.tab20c.colors)
    legend_labels = [f"{label}: {percent}%" for label, percent in zip(attack_types.index, percentages)]
    ax.legend(wedges, legend_labels, title="Attack Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title("Attack Types Distribution")
    ax.set_ylabel("")
    st.pyplot(fig)

# Remaining sections (Trend Visualization, Hypotheses, Conclusions) would be similarly translated.
# Trend Visualization
elif section == "Trend Visualization":
    st.header("📊 Total Casualties by Region")
    st.write(
        """
        This bar chart shows the number of casualties (killed and wounded) due to terrorist attacks by region.
        Each column represents the combined contribution of two categories: killed (red) and wounded (blue).
        """
    )
    region_casualties = df.groupby("Region")[["Num_Killed", "Num_Wounded"]].sum()
    region_casualties["Total_Casualties"] = region_casualties["Num_Killed"] + region_casualties["Num_Wounded"]
    region_casualties = region_casualties.sort_values(by="Total_Casualties", ascending=False)
    region_casualties = region_casualties.drop(columns=["Total_Casualties"])

    fig, ax = plt.subplots(figsize=(12, 8))
    region_casualties.plot(kind="bar", stacked=True, color=["red", "blue"], ax=ax)

    for i, bar_group in enumerate(ax.containers):
        for bar in bar_group:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f"{int(height)}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="white",
                )

    ax.set_title("Total Casualties by Region", fontsize=16)
    ax.set_xlabel("Region", fontsize=12)
    ax.set_ylabel("Number of Casualties", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=10)
    ax.legend(["Killed", "Wounded"], fontsize=10)
    ax.grid(axis="y", alpha=0.5)
    fig.tight_layout()

    st.pyplot(fig)

    st.subheader("📆 Annual Trends in Casualties")
    st.write(
        """
        This line chart illustrates the yearly trend in casualties (killed and wounded),
        offering insights into the historical dynamics of terrorism activity.
        """
    )
    yearly_casualties = df.groupby("Year")[["Num_Killed", "Num_Wounded"]].sum()
    fig = px.line(yearly_casualties, labels={"value": "Number of Casualties", "Year": "Year"})
    st.plotly_chart(fig)

    st.header("📊 Attack Types Over Time")
    st.write(
        """
        This dynamic histogram shows changes in attack types over time. The animation
        enables the visualization of attack distributions by type for each year.
        """
    )
    df_grouped = df.groupby(["Year", "Region", "Attack_Type"]).size().reset_index(name="Count")
    fig = px.bar(
        df_grouped,
        x="Year",
        y="Count",
        color="Region",
        animation_frame="Attack_Type",
        title="Attack Types Over Time",
        labels={"Count": "Number of Attacks", "Year": "Year"},
    )

    fig.update_layout(
        barmode="stack",
        title={"text": "Attack Types Over Time", "x": 0.5, "xanchor": "center"},
        xaxis=dict(title="Year", tickmode="linear"),
        yaxis=dict(title="Number of Attacks"),
    )

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500

    st.plotly_chart(fig)

    st.header("🌍 Global Distribution of Attacks")
    st.write(
        """
        This visualization showcases the geographic distribution of attacks worldwide.
        You can observe how attack types vary by region over the years.
        """
    )
    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="Attack_Type",
        animation_frame="Year",
        title="Global Distribution of Attacks",
        projection="natural earth",
        labels={"Attack_Type": "Attack Type"},
    )

    fig.update_layout(
        title={"text": "Global Distribution of Attacks", "x": 0.5, "xanchor": "center", "yanchor": "top"},
        geo=dict(
            showcoastlines=True,
            coastlinecolor="LightGray",
            showland=True,
            landcolor="whitesmoke",
            showocean=True,
            oceancolor="lightblue",
        ),
    )

    st.plotly_chart(fig)

# Hypothesis: Weapon Choice and Casualties
elif section == "Hypothesis: Weapon Choice and Casualties":
    st.header("🔬 Hypothesis")
    st.write(
        """
        **Hypothesis:** The popularity of certain weapons is related to the number of casualties.
        This section examines statistical relationships between weapon types and casualties.
        """
    )
    st.subheader("🛠️ Weapon Popularity")
    st.write(
        """
        This bar chart shows the distribution of weapon types used in terrorist attacks.
        """
    )
    weapon_counts = df["Weapon_Type"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=weapon_counts.values, y=weapon_counts.index, ax=ax, palette="viridis")
    ax.set_title("Weapon Popularity")
    ax.set_xlabel("Number of Attacks")
    ax.set_ylabel("Weapon Type")
    st.pyplot(fig)

    st.subheader("📊 Weapon Popularity vs Casualties")
    st.write(
        """
        This analysis explores the relationship between average casualty counts and weapon usage frequency.
        The chart combines average casualties with the popularity of weapon types.
        """
    )
    weapon_stats = df.groupby("Weapon_Type").agg(
        avg_casualties=("Total_Casualties", "mean"), usage_count=("Weapon_Type", "count")
    )
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(
        weapon_stats.index,
        weapon_stats["avg_casualties"],
        color="skyblue",
        edgecolor="black",
        label="Average Casualties",
    )
    ax1.set_xlabel("Weapon Type", fontsize=12)
    ax1.set_ylabel("Average Casualties", fontsize=12, color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.set_xticklabels(weapon_stats.index, rotation=45, ha="right")
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()
    ax2.plot(weapon_stats.index, weapon_stats["usage_count"], color="red", marker="o", label="Usage Frequency")
    ax2.set_ylabel("Usage Frequency", fontsize=12, color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.legend(loc="upper right")

    plt.title("Weapon Popularity vs Casualties", fontsize=16)
    fig.tight_layout()
    st.pyplot(fig)

    st.subheader("📐 Statistical Test")
    st.write(
        """
        A t-test is used to compare the average casualty numbers for high and low popularity weapons.
        """
    )
    high_usage = weapon_stats[weapon_stats["usage_count"] > weapon_stats["usage_count"].median()]
    low_usage = weapon_stats[weapon_stats["usage_count"] <= weapon_stats["usage_count"].median()]
    t_stat, p_value = ttest_ind(high_usage["avg_casualties"], low_usage["avg_casualties"])
    st.write(f"**Test Results:** p-value = {p_value:.5f}")

    if p_value > 0.05:
        st.write("🔴 **Hypothesis Rejected:** Weapon choice does not depend on casualty counts.")
    else:
        st.write("🟢 **Hypothesis Confirmed:** Weapon popularity affects casualty numbers.")


# Conclusions
elif section == "Conclusions":
    st.header("📜 Conclusion")
    st.write(
        """
Based on the analysis, the hypothesis that the choice of weapon depends on the average statistical number of victims was refuted. The null hypothesis, which asserts the independence of these variables, could not be rejected. This means that the frequency of choosing a weapon does not depend on the number of victims in terrorist attacks. Therefore, the choice of weapon is most likely determined by other factors that require additional research.
        """
    )
    st.success("🎉 Thank you for using our application! We hope you found it helpful.")
