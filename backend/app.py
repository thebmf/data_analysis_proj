from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from scipy.stats import ttest_ind
import zipfile
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load and preprocess data
# df = pd.read_csv("globalterrorismdb_0718dist.csv", encoding="ISO-8859-1")
path_to_dataset = "globalterrorismdb_0718dist.zip"
with zipfile.ZipFile(path_to_dataset, "r") as z:
    # List all the files in the ZIP archive
    file_names = z.namelist()

    # Assuming there's only one CSV file in the ZIP
    csv_file_name = [name for name in file_names if name.endswith(".csv")][0]

    # Open the CSV file directly
    with z.open(csv_file_name) as f:
        df = pd.read_csv(f, encoding="ISO-8859-1")
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

df["Weapon_Type"] = df["Weapon_Type"].apply(
    lambda x: "Vehicle" if x == "Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)" else x
)


# API Endpoints
@app.get("/data/overview")
def data_overview():
    """Return data overview and statistics."""
    stats = df.describe().to_dict()
    missing = df.isnull().sum().to_dict()
    return {"overview": stats, "missing_values": missing}


@app.get("/data/yearly-trends")
def yearly_trends():
    """Return number of events per year."""
    yearly_counts = df["Year"].value_counts().sort_index().to_dict()
    return {"yearly_counts": yearly_counts}


@app.get("/data/attack-types")
def attack_types():
    """Return distribution of attack types."""
    attack_counts = df["Attack_Type"].value_counts().to_dict()
    return {"attack_counts": attack_counts}


@app.get("/data/weapon-casualties")
def weapon_casualties():
    """Return weapon type statistics and hypothesis results."""
    weapon_stats = df.groupby("Weapon_Type").agg(
        avg_casualties=("Total_Casualties", "mean"), usage_count=("Weapon_Type", "count")
    )
    high_usage = weapon_stats[weapon_stats["usage_count"] > weapon_stats["usage_count"].median()]
    low_usage = weapon_stats[weapon_stats["usage_count"] <= weapon_stats["usage_count"].median()]
    t_stat, p_value = ttest_ind(high_usage["avg_casualties"], low_usage["avg_casualties"])
    return {"weapon_stats": weapon_stats.to_dict(), "p_value": p_value}


@app.get("/data/total-casualties-by-region")
def total_casualties_by_region():
    """Return total casualties (killed and wounded) by region."""
    region_casualties = df.groupby("Region")[["Num_Killed", "Num_Wounded"]].sum()
    region_casualties["Total_Casualties"] = region_casualties["Num_Killed"] + region_casualties["Num_Wounded"]
    region_casualties = region_casualties.sort_values(by="Total_Casualties", ascending=False).to_dict()
    return {"region_casualties": region_casualties}


@app.get("/data/annual-trends-casualties")
def annual_trends_casualties():
    """Return yearly casualties (killed and wounded)."""
    yearly_casualties = df.groupby("Year")[["Num_Killed", "Num_Wounded"]].sum()
    return {"yearly_casualties": yearly_casualties.to_dict()}


@app.get("/data/attack-types-over-time")
def attack_types_over_time():
    """Return attack types distribution over time."""
    df_grouped = df.groupby(["Year", "Attack_Type"]).size().reset_index(name="Count")
    grouped_data = df_grouped.to_dict(orient="records")
    return {"attack_types_over_time": grouped_data}


@app.get("/data/global-distribution")
def global_distribution():
    """Return global distribution of attacks."""
    geo_data = df[["Year", "Latitude", "Longitude", "Attack_Type"]].dropna()
    records = geo_data.to_dict(orient="records")
    return {"global_distribution": records}


@app.get("/data/weapon-analysis")
def weapon_analysis():
    """Return data for weapon popularity and casualties analysis."""
    # Группировка данных
    weapon_stats = (
        df.groupby("Weapon_Type")
        .agg(avg_casualties=("Total_Casualties", "mean"), usage_count=("Weapon_Type", "count"))
        .reset_index()
    )

    # Преобразование в формат словаря
    return {"weapon_stats": weapon_stats.to_dict(orient="records")}


@app.get("/data/weapon-hypothesis-test")
def weapon_hypothesis_test():
    """Perform a statistical test on weapon popularity and casualties."""
    weapon_stats = df.groupby("Weapon_Type").agg(
        avg_casualties=("Total_Casualties", "mean"), usage_count=("Weapon_Type", "count")
    )
    high_usage = weapon_stats[weapon_stats["usage_count"] > weapon_stats["usage_count"].median()]
    low_usage = weapon_stats[weapon_stats["usage_count"] <= weapon_stats["usage_count"].median()]
    t_stat, p_value = ttest_ind(high_usage["avg_casualties"], low_usage["avg_casualties"])
    hypothesis_result = "Confirmed" if p_value <= 0.05 else "Rejected"
    return {"p_value": p_value, "hypothesis_result": hypothesis_result}


@app.get("/api/eda/all-graphs")
def get_all_eda_graphs():
    # Годовые события
    yearly_counts = df["Year"].value_counts().sort_index().to_dict()

    # Топ-10 стран по количеству атак
    top_countries = df["Country"].value_counts().head(10).to_dict()

    # Типы атак
    attack_types = df["Attack_Type"].value_counts().to_dict()

    return {
        "yearly_counts": yearly_counts,
        "top_countries": top_countries,
        "attack_types": attack_types,
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)