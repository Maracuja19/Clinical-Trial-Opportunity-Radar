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

from pathlib import Path

css_path = Path(__file__).parent / "style.css"

with open(css_path, encoding="utf-8") as css_file:
    st.markdown(
        f"<style>{css_file.read()}</style>",
        unsafe_allow_html=True
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

st.divider()



###Top opp ranking"
st.subheader("Top Country-Indication Opportunities")
st.caption("Rank country–indication combinations to identify the highest-scoring opportunities")
if filtered_df.empty:
    st.info("No opportunities match the selected filters.")

else:
    top_opportunities = (
        filtered_df
        .sort_values("opportunity_score", ascending=False)
        .head(15)
        .copy()
    )
    top_opportunities["opportunity"] = (
        top_opportunities["country"]
        + " — "
        + top_opportunities["indication"]
    )

    fig_ranking = px.bar(
        top_opportunities.sort_values(
            "opportunity_score",
            ascending=True
        ),
        x="opportunity_score",
        y="opportunity",
        orientation="h",
        color="opportunity_score",
        color_continuous_scale="Blues",
        labels={
            "opportunity_score": "Opportunity Score",
            "opportunity": "Country — Indication"
        },
        text="opportunity_score"
    )

    fig_ranking.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig_ranking.update_layout(
        yaxis_title="",
        xaxis_title="Opportunity Score",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_ranking, use_container_width=True)



st.divider()


### Map ###
st.subheader("Opportunity Score by Country")
st.caption("Compare overall opportunity scores across countries based on the selected filters")
    
if filtered_df.empty:
    st.info("No opportunities match the selected filters.")
else:
    country_map = (
    filtered_df.groupby("country", as_index=False)
    .agg(
        median_score=("opportunity_score", "median"),
        opportunities=("opportunity_score", "size")
        )
        .reset_index()
        )

country_codes = {
    "Argentina": "ARG",
    "Brazil": "BRA",
    "Chile": "CHL",
    "Colombia": "COL",
    "Ecuador": "ECU",
    "Mexico": "MEX",
    "Paraguay":"PRY",
    "Uruguay": "URY",
    "Venezuela": "VEN"
}

country_map["iso_alpha3"] = country_map["country"].map(country_codes)

fig_map = px.choropleth(
    country_map,
    locations="iso_alpha3",
    locationmode="ISO-3",
    color="median_score",
    range_color=(0, 70),
    hover_name="country",
    hover_data={
        "median_score": ":.2f",
        "opportunities": True,
        "iso_alpha3": False
    },
    color_continuous_scale="Oranges",
)
fig_map.update_geos(
    fitbounds="locations",
    visible=True,
    showcountries=True,
    showcoastlines=True
)
fig_map.update_layout(
    margin={"r":0, "t":0, "l":0, "b":0},
    coloraxis_colorbar_title="Median Score"
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()


col_heatmap, col_scatter = st.columns(2)

with col_heatmap:
### TA heatmap ###
    st.subheader("Opportunity Score by Country & TA")
    st.caption(
    "Identify therapeutic areas with higher opportunity scores across countries"
    )
    if filtered_df.empty:
        st.info("No opportunities match the selected filters")
    else:
        heatmap_data = filtered_df.pivot_table(
            index="country",
            columns="therap_area",
            values="opportunity_score",
            aggfunc="median"
        )
        fig_heatmap = px.imshow(
            heatmap_data,
            labels={
                "x": "Therapeutic Area",
                "y": "Country",
                "color": "Median Opportunity Score"
            },
            color_continuous_scale="Oranges",
            aspect="auto",
            text_auto=".1f"
        )

        fig_heatmap.update_layout(
            xaxis_title="Therapeutic Area",
            yaxis_title="Country"
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

with col_scatter:
### Population vs. opp score ###
    st.subheader("Opportunity Score vs. Patient Population")
    st.caption("Explore the relationship between patient population and opportunity scores across selected opportunities")

    fig_scatter = px.scatter(
        filtered_df,
        x="patient_pop",
        y="opportunity_score"
    )
    fig_scatter = px.scatter(
        filtered_df,
        x="patient_pop",
        y="opportunity_score",
        color="therap_area"
    )
    fig_scatter = px.scatter(
        filtered_df,
        x="patient_pop",
        y="opportunity_score",
        color="therap_area",
        hover_data=[
            "country",
            "indication",
            "patient_pop",
            "opportunity_score"
        ],
        color_discrete_sequence=[
                "#A78BFA",  
                "#3767CE",  
                "#FFFFFF",  
                "#F1A44C",  
                "#7DC9E9"   
            ]
    )
    
    fig_scatter.update_layout(
        xaxis_title="Patient Population",
        yaxis_title="Opportunity Score",
        legend_title="Therapeutic Area"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

##ä Opp details ###
st.subheader("Opportunity Details")
st.caption("Review the metrics and opportunity scores for each country–indication combination")

display_columns = [
    "country",
    "therap_area",
    "indication",
    "patient_pop",
    "unmet_need",
    "trial_compet",
    "op_feas",
    "reg_env",
    "opportunity_score"
]

st.dataframe(
    filtered_df[display_columns].rename(columns={
        "country": "Country",
        "therap_area": "Therapeutic Area",
        "indication": "Indication",
        "patient_pop": "Patient Population",
        "unmet_need": "Unmet Need",
        "trial_compet": "Trial Competition",
        "op_feas": "Operational Feasibility",
        "reg_env": "Regulatory Environment",
        "opportunity_score": "Opportunity Score"
    }),
    use_container_width=True,
    hide_index=True
)
csv_data = filtered_df[display_columns].rename(columns={
    "country": "Country",
    "therap_area": "Therapeutic Area",
    "indication": "Indication",
    "patient_pop": "Patient Population",
    "unmet_need": "Unmet Need",
    "trial_compet": "Trial Competition",
    "op_feas": "Operational Feasibility",
    "reg_env": "Regulatory Environment",
    "opportunity_score": "Opportunity Score"
}).to_csv(index=False)

st.download_button(
    label="Download filtered opportunities",
    data=csv_data,
    file_name="filtered_opportunities.csv",
    mime="text/csv"
)

st.divider()

st.header("Methodology & Limitations")

st.subheader("Scoring Methodology")

st.caption("""
Each country–indication combination is evaluated using 5 factors: patient population, unmet medical need, trial competition,
operational feasibility, and regulatory environment.

The factors are normalized to a 0–1 scale and combined into a weighted score from 0 to 100. 

Lower trial competition contributes
positively to the score, while higher values in the other 4 factors increase it.
""")

st.subheader("Model Limitations")

st.caption("""
The dataset is synthetic and does not represent actual epidemiological, regulatory, or clinical-trial data.

The opportunity score is a relative prioritization metric based on predefined weights, not a probability of clinical-trial success.
""")