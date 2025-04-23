import pandas as pd
import streamlit as st
from PIL import Image

# Load and display logo
logo = Image.open("USA_Baseball_team_logo.png")
st.image(logo, width=200)  # Adjust width as needed

st.title("PDP Premier Players Dashboard")

# Load CSV
df = pd.read_csv("pdp_premier.csv")

# Rename "Year" to "HS Grad Year"
df = df.rename(columns={"Year": "HS Grad Year"})

# Drop unnecessary columns
df = df.drop(columns=["Last Name", "First Name", "BirthDate", "25 Total", "NAS CMJ Height",	"NAS Peak Power[W]", "NAS Peak Power BM[W/Kg]",	"AS CMJ Height", "AS Peak Power[W]", "AS Peak Power BM[W/Kg]", "Drift Power Delta %", "ABSVAL DPWR Delta"], errors="ignore")

# Ensure "30 Total" is numeric
df["30 Total"] = pd.to_numeric(df["30 Total"], errors="coerce")

# Drop rows with missing values in key columns
df = df.dropna(subset=["NAME", "Location", "HS Grad Year", "Event", "Event Type", "30 Total"])

# Sidebar Filters
st.sidebar.header("Filter Player Data")

location = st.sidebar.selectbox("Select Location", ["All"] + sorted(df["Location"].unique()))
name = st.sidebar.selectbox("Select Player", ["All"] + sorted(df["NAME"].unique()))
grad_year = st.sidebar.selectbox("Select HS Grad Year", ["All"] + sorted(df["HS Grad Year"].unique()))
event = st.sidebar.selectbox("Select Event", ["All"] + sorted(df["Event"].unique()))
event_type = st.sidebar.selectbox("Select Event Type", ["All"] + sorted(df["Event Type"].unique()))

# Slider for 30 Total
min_30 = round(df["30 Total"].min(), 2)
max_30 = round(df["30 Total"].max(), 2)
avg_30 = round(df["30 Total"].mean(), 2)

st.sidebar.markdown(f"**Average 30 Total: {avg_30} sec**")

thirty_total_range = st.sidebar.slider(
    "30 Total Range (sec)",
    min_value=min_30,
    max_value=max_30,
    value=(min_30, max_30),
    step=0.01
)

# Apply filters
filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location]

if name != "All":
    filtered_df = filtered_df[filtered_df["NAME"] == name]

if grad_year != "All":
    filtered_df = filtered_df[filtered_df["HS Grad Year"] == grad_year]

if event != "All":
    filtered_df = filtered_df[filtered_df["Event"] == event]

if event_type != "All":
    filtered_df = filtered_df[filtered_df["Event Type"] == event_type]

# Apply slider filter
filtered_df = filtered_df[
    (filtered_df["30 Total"] >= thirty_total_range[0]) & 
    (filtered_df["30 Total"] <= thirty_total_range[1])
]

# Show result
st.dataframe(filtered_df)
