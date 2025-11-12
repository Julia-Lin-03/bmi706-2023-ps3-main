import altair as alt
import pandas as pd
import streamlit as st

### P1.2 ###
@st.cache
def load_data():
    cancer_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/cancer_ICD10.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Cancer", "Sex"],
    var_name="Age",
    value_name="Deaths",
)
    pop_df = pd.read_csv("https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/population.csv").melt(  # type: ignore
    id_vars=["Country", "Year", "Sex"],
    var_name="Age",
    value_name="Pop",
)
    df = pd.merge(left=cancer_df, right=pop_df, how="left")
    df["Pop"] = df.groupby(["Country", "Sex", "Age"])["Pop"].fillna(method="bfill")
    df.dropna(inplace=True)

    df = df.groupby(["Country", "Year", "Cancer", "Age", "Sex"]).sum().reset_index()
    df["Rate"] = df["Deaths"] / df["Pop"] * 100_000
    return df

df = load_data()

st.write("## Age-specific cancer mortality rates")
### P1.2 ###


### P2.1 ###
year = st.slider(
    "Select Year", 
    int(df["Year"].min()),   
    int(df["Year"].max()),   
    2012                     
)

subset = df[df["Year"] == year]
### P2.1 ###


### P2.2 ###
sex = st.radio(
    "Select Sex",
    options=sorted(df["Sex"].unique()),  
    index=1                              
)

subset = subset[subset["Sex"] == sex]
### P2.2 ###


### P2.3 ###
countries = st.multiselect(
    "Select Countries",
    options=sorted(df["Country"].unique()),
    default=["Austria", "Germany", "Iceland", "Spain", "Sweden", "Thailand", "Turkey"]
)

subset = subset[subset["Country"].isin(countries)]
### P2.3 ###


### P2.4 ###
cancer = st.selectbox(
    "Select Cancer Type",
    options=sorted(df["Cancer"].unique()),
    index=sorted(df["Cancer"].unique()).index("Malignant neoplasm of stomach")
    if "Malignant neoplasm of stomach" in df["Cancer"].unique()
    else 0
)

subset = subset[subset["Cancer"] == cancer]
### P2.4 ###


### P2.5 ###
chart = (
    alt.Chart(subset)
    .mark_rect()
    .encode(
        x=alt.X("Country:N", title="Country", sort=sorted(subset["Country"].unique())),
        y=alt.Y("Cancer:N", title="Cancer Type"),
        color=alt.Color(
            "mean(Rate):Q",
            title="Mortality Rate per 100k (log scale)",
            scale=alt.Scale(type="log", domain=[0.01, 1000], clamp=True),
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="Country"),
            alt.Tooltip("Cancer:N", title="Cancer"),
            alt.Tooltip("mean(Rate):Q", title="Mean Rate per 100k", format=",.2f"),
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("Sex:N", title="Sex"),
        ],
    )
    .properties(
        title="Cancer Mortality Rate Heatmap",
        width=600,
        height=500,
    )
)

st.altair_chart(chart, use_container_width=True)
### P2.5 ###
