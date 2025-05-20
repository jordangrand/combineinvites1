import pandas as pd
import streamlit as st
from PIL import Image

# Load and display logo
logo = Image.open("USA_Baseball_team_logo.png")
st.image(logo, width=200)

st.title("Combine Invites PDP Testing")

# Load CSV
df = pd.read_csv("DraftCombinePDPData2.0.csv")

# Rename "Year" to "HS Grad Year"
df = df.rename(columns={"Year": "HS Grad Year"})

# Drop unnecessary columns
df = df.drop(columns=[
    "Last Name", "First Name", "DPL ID", "BirthDate", "25 Total", "Agility Diff", "% Change", "Drift GCT Delta %", "Drift Used Area Delta %", "ABSVAL DUA Delta",
    "NAS CMJ Height", "NAS Peak Power[W]", "NAS Peak Power BM[W/Kg]",
    "AS CMJ Height", "AS Peak Power[W]", "AS Peak Power BM[W/Kg]",
    "Drift Power Delta %", "ABSVAL DPWR Delta"
], errors="ignore")

# Define numeric columns to convert and round
numeric_cols = [
    "Height (in)", "Weight",
    "10 yd Split (sec)", "20 yd Split(sec)", "30 Total",
    "Green Box", "Green 3",
    "BJ Distance (ft)", "BJ Distance (in)",
    "CMJ GCT[sec]", "CMJ Height[in]", "Max CMJ Height[in]",
    "Peak Power[W]", "Peak Power BM[W/Kg]",
    "LEFT DOWN", "LEFT 90", "LEFT UP", "RIGHT DOWN", "RIGHT 90", "RIGHT UP"
]

# Convert to numeric and round
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_cols] = df[numeric_cols].round(1)


# Sidebar Filters
st.sidebar.header("Filter Player Data")

location = st.sidebar.selectbox("Select Location", ["All"] + sorted(df["Location"].unique()))
name = st.sidebar.selectbox("Select Player", ["All"] + sorted(df["NAME"].unique()))
grad_year = st.sidebar.selectbox("Select HS Grad Year", ["All"] + sorted(df["HS Grad Year"].unique()))
event = st.sidebar.selectbox("Select Event", ["All"] + sorted(df["Event"].unique()))
event_type = st.sidebar.selectbox("Select Event Type", ["All"] + sorted(df["Event Type"].unique()))

# Optional: 30 Total
use_30_slider = st.sidebar.checkbox("Filter by 30 Total", value=False)
if use_30_slider:
    min_30 = df["30 Total"].min()
    max_30 = df["30 Total"].max()
    avg_30 = df["30 Total"].mean()
    st.sidebar.markdown(f"**Average 30 Total: {avg_30:.1f} sec**")
    thirty_total_range = st.sidebar.slider(
        "30 Total Range (sec)",
        min_value=float(min_30),
        max_value=float(max_30),
        value=(float(min_30), float(max_30)),
        step=0.1
    )

# Optional: Peak Power
use_power_slider = st.sidebar.checkbox("Filter by Peak Power", value=False)
if use_power_slider:
    min_power = df["Peak Power[W]"].min()
    max_power = df["Peak Power[W]"].max()
    avg_power = df["Peak Power[W]"].mean()
    st.sidebar.markdown(f"**Average Peak Power: {avg_power:.1f} W**")
    power_range = st.sidebar.slider(
        "Peak Power Range (W)",
        min_value=float(min_power),
        max_value=float(max_power),
        value=(float(min_power), float(max_power)),
        step=1.0
    )

# Optional: Peak Power BM
use_powerbm_slider = st.sidebar.checkbox("Filter by Peak Power BM (W/Kg)", value=False)
if use_powerbm_slider:
    min_powerbm = df["Peak Power BM[W/Kg]"].min()
    max_powerbm = df["Peak Power BM[W/Kg]"].max()
    avg_powerbm = df["Peak Power BM[W/Kg]"].mean()
    st.sidebar.markdown(f"**Avg Peak Power BM: {avg_powerbm:.1f} W/Kg**")
    powerbm_range = st.sidebar.slider(
        "Peak Power BM Range (W/Kg)",
        min_value=float(min_powerbm),
        max_value=float(max_powerbm),
        value=(float(min_powerbm), float(max_powerbm)),
        step=0.1
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

if use_30_slider:
    filtered_df = filtered_df[
        (filtered_df["30 Total"] >= thirty_total_range[0]) &
        (filtered_df["30 Total"] <= thirty_total_range[1])
    ]

if use_power_slider:
    filtered_df = filtered_df[
        (filtered_df["Peak Power[W]"] >= power_range[0]) &
        (filtered_df["Peak Power[W]"] <= power_range[1])
    ]

if use_powerbm_slider:
    filtered_df = filtered_df[
        (filtered_df["Peak Power BM[W/Kg]"] >= powerbm_range[0]) &
        (filtered_df["Peak Power BM[W/Kg]"] <= powerbm_range[1])
    ]

# Display results
st.subheader("Filtered Results")
st.dataframe(filtered_df)
