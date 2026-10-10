import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("opportunities_scored.csv")

### Page config ###
st.set_page_config(
    page_title = "Clinical Trials Opportunity Radar",
    page_icon="",
    layout="wide"
)


#dashboard title
st.title("Clinical Trials Opportunity Radar")
st.caption("Country & Indication Opportunity Assessment")


### Filters ###
st.sidebar.header("Filters")
countries = ["All Countries"] + sorted(df["country"].unique().tolist())
areas = ["All Areas"] + sorted(df["therap_area"].unique().tolist())
indications = ["All Indications"] + sorted(df["indication"].unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Country",
    options=countries,
    default=countries
)
selected_areas = st.sidebar.multiselect(
    "Therapeutic Area",
    options=areas,
    default=areas
)
filtered_df = df[
    df["country"].isin(selected_countries)
    & df["therap_area"].isin(selected_areas)
].copy()

#indication funnel
available_indications = sorted(
    filtered_df["indication"].unique().tolist()
)

selected_indications = st.sidebar.multiselect(
    "Indication",
    options=available_indications,
    default=available_indications
)

#apply filters
filtered_df = filtered_df[
    filtered_df["indication"].isin(selected_indications)
].copy()

st.write(f"**Opportunities matching filters:** {len(filtered_df)}")


### KPIs ###
st.subheader("Overview")

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Countries",
        filtered_df["country"].nunique()
    )
with col2:
    st.metric(
        "Indications",
        filtered_df["indication"].nunique()
    )
with col3:
    st.metric(
        "Opportunities",
        len(filtered_df)
    )
